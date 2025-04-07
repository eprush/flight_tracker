from typing import Iterable, Sized
from parsing.abstract_parser import AbstractParser, Model, Flight_info


class AviationStackParser(AbstractParser):
    def __init__(self, seq: dict):
        self.data: Iterable | Sized = seq["data"]


    def get(self) -> tuple[Flight_info, ...]:
        result = tuple(Model(airline= "", code_icao= "", aircraft= "")
                       for _ in range(len(self.data)))
        for i, flight in enumerate(self.data):
            flight_data = result[i]
            aircraft = flight["aircraft"]["modelText"]
            code_icao = flight["flight"]["icao"]
            airline = flight["airline"]["name"] if flight["airline"]["name"]\
                    else flight["flight"]["codeshared"]["airline_name"]
            #callsign = flight[]
            #lat, lon =

            flight_data["aircraft"] = aircraft
            flight_data["code_icao"] = code_icao
            flight_data["airline"] = airline
            #flight_data["callsign"] = callsign
        return result
