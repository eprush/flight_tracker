from loading import load_data
from parsing.aviastack_parser import AviationStackParser
from repositories.csv_repository import CSVRepository
from models.flight_data import FlightData
from config import params_iterator

if __name__ == "__main__":
    repo = CSVRepository("aviastack.csv", FlightData)
    for params in params_iterator:
        data = load_data(params)
        parser = AviationStackParser(data)
        for flight in parser.get():
            repo.add(flight)
