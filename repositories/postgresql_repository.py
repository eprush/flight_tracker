"""
The module describes a repository running using the PostgreSQL database management system
"""
import psycopg2
from datetime import datetime
from inspect import get_annotations
from typing import Any, Callable

from config import password
from repositories.abstract_repository import AbstractRepository, T


Cursor = psycopg2.extensions.cursor
UsingCursor = Callable[[Cursor, ...], ...]

#decorator
def connect_to(db: str = ""):
    if db:
        con = psycopg2.connect(
            user="postgres",
            password=password,
            host="127.0.0.1",
            port="5432",
            database=db
        )
    else:
        con = psycopg2.connect(
            user="postgres",
            password=password,
            host="127.0.0.1",
            port="5432",
        )
        con.autocommit = True

    def inner_decorator(f: UsingCursor):
        def wrapper(*args):
            cur = con.cursor()
            try:
                result = f(cur, *args)
            finally:
                cur.close()
                con.close()
            return result
        return wrapper
    return inner_decorator

def which(type_data) -> str:
    types = {int: "INTEGER NOT NULL",
             str: "TEXT NOT NULL",
             (int | None): "INTEGER",
             datetime: "TIMESTAMP"}
    return types[type_data]

class PostgreSQLRepository(AbstractRepository[T]):
    """
    A repository that works with the PostgreSQL database management system
    """

    def __init__(self, db_file: str, cls: type):
        self.db_file = db_file
        self.content_class = cls
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop("id")

        @connect_to()
        def create_db(cursor: Cursor) -> None:
            try:
                cursor.execute("CREATE DATABASE %s;" % (self.db_file,))
            except psycopg2.errors.DuplicateDatabase:
                print("the database already exists")

        @connect_to(db=self.db_file)
        def create_table_with(cursor: Cursor, table_name:str, fields: dict) -> None:
            str_types = "".join(f",\n%s {which(field_type)}" for field_type in fields.values())
            cursor.execute(f"CREATE TABLE {table_name} (id SERIAL PRIMARY KEY {str_types});",
                tuple(fields.keys())
            )
            print(f"table {table_name} is created")
        create_db()
        create_table_with(self.table_name, self.fields)

    def add(self, obj: T) -> int:
        if getattr(obj, 'id', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `id` attribute')

        adding_fields = ", ".join(self.fields.keys())
        v = ", ".join("%s" * len(self.fields))

        @connect_to(db=self.db_file)
        def add_into(cursor: Cursor, table_name:str, fields: dict) -> int:
            values = tuple(getattr(obj, attr) for attr in fields.keys())
            if values:
                cursor.execute(f"INSERT INTO {table_name} ({adding_fields}) VALUES ({v})", values)
            else:
                cursor.execute(f"INSERT INTO {table_name} DEFAULT VALUES")
            id_ = cursor.lastrowid if cursor.lastrowid is not None else 0
            return id_
        obj.id = add_into(self.table_name, self.fields)
        return obj.id

    def get(self, id_: int) -> T | None:
        @connect_to(db=self.db_file)
        def get_from(cursor: Cursor, table_name: str) -> list:
            cursor.execute(f"SELECT * FROM {table_name} WHERE id == %s;", (id_,))
            return cursor.fetchone()
        params = get_from(self.table_name)
        return self.content_class(*params) if params is not None else None

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        @connect_to(db=self.db_file)
        def get_all_from(cursor: Cursor, table_name: str) -> list[tuple]:
            if where is None:
                cursor.execute(f"SELECT * FROM {table_name}")
            else:
                str_where = " AND ".join(f"{attr} = %s " for attr in where.keys())
                cursor.execute(f"SELECT * FROM {table_name} WHERE {str_where}", tuple(where.values()))
            res = cursor.fetchall()
            return res
        return [self.content_class(*item) for item in get_all_from(self.table_name)]

    def update(self, obj: T) -> None:
        @connect_to(db=self.db_file)
        def is_updated_into(cursor: Cursor, table_name: str, fields: dict) -> bool:
            has_id_request = f"SELECT * FROM {table_name} WHERE id == %s;"
            cursor.execute(has_id_request, (obj.id,))
            has_id = cursor.fetchone() is not None
            if has_id and len(fields.keys()):
                setting_fields = ", ".join(f"{field} = %s" for field in fields.keys())
                values = tuple(getattr(obj, attr) for attr in fields.keys()) + (obj.id,)
                cursor.execute(f"UPDATE {table_name} SET {setting_fields} WHERE id == %s;", values)
            return has_id
        if is_updated_into(self.table_name, self.fields):
            return
        raise ValueError('attempt to update object with unknown id')

    def delete(self, id_: int) -> None:
        @connect_to(db=self.db_file)
        def is_deleted_from(cursor: Cursor, table_name: str):
            has_id_request = f"SELECT * FROM {table_name} WHERE id = %s"
            cursor.execute(has_id_request, (id_,))
            has_id = cursor.fetchone() is not None
            if has_id:
                cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (id_,))
            return has_id
        if is_deleted_from(self.table_name):
            return
        raise KeyError

if __name__ == "__main__":
    class Custom:
        id: int = 0

    storage = PostgreSQLRepository("test_db", Custom)
    storage.add(Custom())