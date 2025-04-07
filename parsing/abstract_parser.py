from abc import ABC, abstractmethod
from typing import TypeVar, TypedDict, Iterable


class Model(TypedDict):  # pylint: disable=too-few-public-methods
    """
    Модель должна содержать атрибут pk
    """
    #callsign: str
    code_icao: str
    aircraft: str
    airline: str
    #lat: float
    #lon: float


Flight_info = TypeVar('Flight_info', bound=Model)

class AbstractParser(ABC):
    """
    Abstract parser.
    Abstract methods:
    __init__
    get
    """

    @abstractmethod
    def __init__(self, seq: Iterable):
        """
        :param seq: data from third-party source
        """

    @abstractmethod
    def get(self) -> tuple[Flight_info, ...]:
        """
        Gets all the parameters. If there are no at least one necessary parameter, it raises an ValueError.
        :return:
        """