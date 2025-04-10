from config.loading import load_data
from parsing.aviastack_parser import AviationStackParser
#from repositories.csv_repository import CSVRepository
from repositories.postgresql_repository import PostgreSQLRepository
from models.flight_data import FlightData
from config.config import params_iterator, postgreSQL_db_name

if __name__ == "__main__":
    repo = PostgreSQLRepository(postgreSQL_db_name, FlightData)
    for params in params_iterator:
        data = load_data(params)
        parser = AviationStackParser(data)
        for flight in parser.get():
            repo.add(flight)
