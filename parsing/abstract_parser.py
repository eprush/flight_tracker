from abc import ABC, abstractmethod
from typing import TypeVar, Iterable, Protocol


class FlightInfo(Protocol):  # pylint: disable=too-few-public-methods
    #callsign: str
    code_icao: str
    aircraft: str
    airline: str
    #lat: float
    #lon: float


T = TypeVar('T', bound=FlightInfo)

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
    def get(self) -> tuple[T, ...]:
        """
        Gets all the parameters. If there are no at least one necessary parameter, it raises an ValueError.
        :return:
        """