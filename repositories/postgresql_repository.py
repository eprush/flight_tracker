"""
The module describes a repository running using the PostgreSQL database management system
"""
import psycopg2
from datetime import datetime
from inspect import get_annotations
from typing import Any, Callable
from contextlib import closing

from config import password
from repositories.abstract_repository import AbstractRepository, T


Cursor = psycopg2.extensions.cursor
UsingCursor = Callable[[Cursor, ...], ...]

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
        def create_table(cursor: Cursor) -> None:
            str_types = "".join(f",\n%s {which(field_type)}" for field_type in self.fields.values())
            cursor.execute(f"CREATE TABLE {self.table_name} (id SERIAL PRIMARY KEY {str_types});",
                tuple(self.fields.keys())
            )
            print(f"table {self.table_name} is created")
        create_db()
        create_table()

    def add(self, obj: T) -> int:
        if getattr(obj, 'id', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `id` attribute')

        @connect_to(db=self.db_file)
        def add(cursor: Cursor) -> int:
            names = ", ".join(self.fields.keys())
            p = ", ".join("%s" * len(self.fields))
            values = tuple(getattr(obj, attr) for attr in self.fields.keys())
            if values:
                cursor.execute(f"INSERT INTO {self.table_name} ({names}) VALUES ({p})", values)
            else:
                cursor.execute(f"INSERT INTO {self.table_name} DEFAULT VALUES")
            id_ = cursor.lastrowid if cursor.lastrowid is not None else 0
            print(id_)
            return id_
        obj.id = add()
        return obj.id

    def get(self, id_: int) -> T | None:
        @connect_to(db=self.db_file)
        def get(cursor: Cursor) -> T | None:
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE id == %s;", (id_,))
            params = cursor.fetchone()
            obj = self.content_class(*params) if params is not None else None
            return obj
        return get()

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        @connect_to(db=self.db_file)
        def get_all(cursor: Cursor) -> list[tuple]:
            if where is None:
                cursor.execute(f"SELECT * FROM {self.table_name}")
            else:
                str_where = " AND ".join(f"{attr} = %s " for attr in where.keys())
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE {str_where}", tuple(where.values()))
            res = cursor.fetchall()
            return res
        return [self.content_class(*item) for item in get_all()]

    def update(self, obj: T) -> None:
        @connect_to(db=self.db_file)
        def is_updated(cursor: Cursor):
            has_id_request = f"SELECT * FROM {self.table_name} WHERE id == %s;"
            cursor.execute(has_id_request, (obj.id,))
            has_id = cursor.fetchone() is not None
            if has_id and len(self.fields.keys()):
                fields = ", ".join(f"{field} = %s" for field in self.fields.keys())
                values = tuple(getattr(obj, attr) for attr in self.fields.keys()) + (obj.id,)
                cursor.execute(f"UPDATE {self.table_name} SET {fields} WHERE id == %s;", values)
            return has_id
        if is_updated():
            return
        raise ValueError('attempt to update object with unknown id')

    def delete(self, id_: int) -> None:
        @connect_to(db=self.db_file)
        def is_deleted(cursor: Cursor):
            has_id_request = f"SELECT * FROM {self.table_name} WHERE id = %s"
            cursor.execute(has_id_request, (id_,))
            has_id = cursor.fetchone() is not None
            if has_id:
                cursor.execute(f"DELETE FROM {self.table_name} WHERE id = %s", (id_,))
            return has_id
        if is_deleted():
            return
        raise KeyError

if __name__ == "__main__":
    class Custom:
        id: int = 0

    storage = PostgreSQLRepository("test_db", Custom)
    storage.add(Custom())