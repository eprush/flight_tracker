from inspect import get_annotations
from itertools import count
from typing import Any
import pandas as pd

from .abstract_repository import AbstractRepository, T

class Data(pd.DataFrame):
    def __iter__(self):
        return (self.loc[i] for i in range(len(self)))

class CSVRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: type):
        self.db_file = db_file

        self.content_class = cls
        self.fields = get_annotations(cls, eval_str=True)

        #save repository file
        df = pd.DataFrame({field: [] for field in self.fields.keys()})
        df.to_csv(self.db_file, encoding="utf-8", index=False)
        self.fields.pop("id")

        self._counter = count(1)

    def get(self, id_: int) -> T | None:
        flights = pd.read_csv(self.db_file, encoding="utf-8")
        try:
            obj = flights.loc[id_ - 1]
        except KeyError:
            return None
        return self.content_class(*obj)

    def add(self, obj: T) -> int:
        if getattr(obj, 'id', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `id` attribute')
        flights = pd.read_csv(self.db_file, encoding="utf-8")
        id_ = next(self._counter)
        values = [id_] + [getattr(obj, field) for field in self.fields.keys()]
        flights.loc[id_] = values
        flights.to_csv(self.db_file, encoding="utf-8", index=False)
        obj.id = id_
        return id_

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        flights = Data(pd.read_csv(self.db_file, encoding="utf-8"))
        if where is None:
            return [self.content_class(*row) for row in flights]
        result = []
        for row in flights:
            obj = self.content_class(*row)
            if all(getattr(obj, attr) == value for attr, value in where.items()):
                result.append(obj)
        return result

    def update(self, obj: T) -> None:
        id_ = obj.id
        if id_ == 0:
            raise ValueError('attempt to update object with unknown id')
        values = [id_] + [getattr(obj, field) for field in self.fields.keys()]
        flights = pd.read_csv(self.db_file, encoding="utf-8")
        flights.loc[id_ - 1] = values
        flights.to_csv(self.db_file, encoding="utf-8", index=False)

    def delete(self, id_: int) -> None:
        flights = pd.read_csv(self.db_file, encoding="utf-8")
        flights.drop(id_ - 1, inplace=True)
        flights.to_csv(self.db_file, encoding="utf-8", index=False)