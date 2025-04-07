from loading import load_data
from parsing.aviastack_parser import AviationStackParser
from repositories.csv_repository import CSVRepository
from models.flight_data import Data

if __name__ == "__main__":
    parser = AviationStackParser(load_data())
    repo = CSVRepository("aviastack.csv", Data)
    for flight in parser.get():
        repo.add(flight)
