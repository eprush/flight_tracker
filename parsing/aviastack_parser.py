from typing import Iterable, Sized
from parsing.abstract_parser import AbstractParser, T
from models.flight_data import Data
from config import bounds

def is_in_bounds(lat, lon):
    return bounds["min_latitude"] <= lat <= bounds["max_latitude"] and bounds["min_longitude"] <= lon <= bounds["max_longitude"]

class AviationStackParser(AbstractParser):
    def __init__(self, seq: dict):
        self.data: Iterable | Sized = seq["data"]

    def get(self) -> tuple[T, ...]:
        result = []
        for i, flight in enumerate(self.data):
            flight_data = Data(aircraft="", airline="", code_icao="", lat=float("inf"), lon=float("inf"), callsign="")
            try:
                lat = flight["live"]["latitude"]
                print(lat)
                lon = flight["live"]["longitude"]
                print(lon)

                aircraft = flight["aircraft"]["registration"]
                print(aircraft)

                code_icao = flight["flight"]["icao"]
                print(code_icao)

                airline = flight["airline"]["name"] if flight["airline"] and flight["airline"]["name"] \
                    else flight["flight"]["codeshared"]["airline_name"]
                print(airline)
            except KeyError:
                print("KeyError")
                continue
            except TypeError:
                print("TypeError")
                continue

            try:
                callsign = flight["callsign"]
                callsign = callsign if callsign is not None else ""
                flight_data.callsign = callsign
                print(callsign)
            except KeyError:
                print("Сallsign not found")

            lat = float(lat) if lat is not None else float("inf")
            lon = float(lon) if lon is not None else float("inf")
            if not is_in_bounds(lat, lon):
                continue

            flight_data.lat = lat
            flight_data.lon = lon
            flight_data.aircraft = aircraft if aircraft is not None else ""
            flight_data.code_icao = code_icao if code_icao is not None else ""
            flight_data.airline = airline if airline is not None else ""
            result.append(flight_data)
        return tuple(result)
