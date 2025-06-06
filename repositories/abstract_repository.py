"""
Модуль содержит описание абстрактного репозитория

Репозиторий реализует хранение объектов, присваивая каждому объекту уникальный
идентификатор в атрибуте id. Объекты, которые могут быть сохранены
в репозитории, должны поддерживать добавление атрибута id и не должны
использовать его для иных целей.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Protocol, Any


class Model(Protocol):  # pylint: disable=too-few-public-methods
    """
    Модель должна содержать атрибут id
    """
    id: int


T = TypeVar('T', bound=Model)


class AbstractRepository(ABC, Generic[T]):
    """
    Абстрактный репозиторий.
    Абстрактные методы:
    add
    get
    get_all
    update
    delete
    """

    @abstractmethod
    def add(self, obj: T) -> int:
        """
        Добавить объект в репозиторий, вернуть id объекта,
        также записать id в атрибут id.
        """

    @abstractmethod
    def get(self, id_: int) -> T | None:
        """ Получить объект по id. Если такого id нет, то вернуть None. """

    @abstractmethod
    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """

    @abstractmethod
    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле id. """

    @abstractmethod
    def delete(self, id_: int) -> None:
        """ Удалить запись """
