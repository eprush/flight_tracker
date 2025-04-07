from typing import Iterable, Sized
from parsing.abstract_parser import AbstractParser, T
from models.flight_data import Data


class AviationStackParser(AbstractParser):
    def __init__(self, seq: dict):
        self.data: Iterable | Sized = seq["data"]


    def get(self) -> tuple[T, ...]:
        result = tuple(Data(
            airline="",
            code_icao="",
            aircraft="",
            lat=float("inf"),
            lon=float("inf")
            )
            for _ in range(len(self.data)))

        for i, flight in enumerate(self.data):
            flight_data = result[i]
            try:
                aircraft = flight["aircraft"]["modelText"]
                code_icao = flight["flight"]["icao"]
                airline = flight["airline"]["name"] if flight["airline"]["name"] \
                    else flight["flight"]["codeshared"]["airline_name"]
                # callsign = flight[]
                lat = flight["live"]["latitude"]
                lon = flight["live"]["longitude"]
            except KeyError:
                continue
            except TypeError:
                continue

            flight_data.aircraft = aircraft if aircraft is not None else ""
            flight_data.code_icao = code_icao if code_icao is not None else ""
            flight_data.airline = airline if airline is not None else ""
            flight_data.lat = float(lat) if lat is not None else float("inf")
            flight_data.lon = float(lon) if lon is not None else float("inf")
            #flight_data.callsign = callsign
        return result
