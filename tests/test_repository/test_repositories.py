from repositories.csv_repository import CSVRepository
from repositories.postgresql_repository import PostgreSQLRepository

import pytest
from dataclasses import dataclass

@dataclass(eq=True)
class Custom:
    id: int = 0

@pytest.fixture()
def custom_class():
    return Custom

@pytest.mark.parametrize("repo", (CSVRepository("test_db_file.csv", Custom),
                                  PostgreSQLRepository('test_db', Custom)))
def test_crud(repo, custom_class):
    obj = custom_class() #Custom(id=0)
    id_ = repo.add(obj) # 1
    assert obj.id == id_
    assert repo.get(id_) == obj
    obj2 = custom_class()
    obj2.id = id_
    repo.update(obj2)
    assert repo.get(id_) == obj2
    repo.delete(id_)
    assert repo.get(id_) is None


@pytest.mark.parametrize("repo", (CSVRepository("test_db_file.csv", Custom),
                                  PostgreSQLRepository('test_db', Custom)))
def test_cannot_add_with_id(repo, custom_class):
    obj = custom_class()
    obj.id = 1
    with pytest.raises(ValueError):
        repo.add(obj)


@pytest.mark.parametrize("repo", (CSVRepository("test_db_file.csv", Custom),
                                  PostgreSQLRepository('test_db', Custom)))
def test_cannot_add_without_id(repo):
    with pytest.raises(ValueError):
        repo.add(0)


@pytest.mark.parametrize("repo", (CSVRepository("test_db_file.csv", Custom),
                                  PostgreSQLRepository('test_db', Custom)))
def test_cannot_delete_unexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(-1)


@pytest.mark.parametrize("repo", (CSVRepository("test_db_file.csv", Custom),
                                  PostgreSQLRepository('test_db', Custom)))
def test_cannot_update_without_id(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)


@pytest.mark.parametrize("repo", (CSVRepository("test_db_file.csv", Custom),
                                  PostgreSQLRepository("test_db", Custom)))
def test_get_all(repo, custom_class):
    objects = [custom_class() for _ in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects