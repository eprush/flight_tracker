from dataclasses import dataclass


@dataclass
class FlightData:
    callsign: str
    code_icao: str
    aircraft: str
    airline: str
    lat: float
    lon: float
    id: int = 0