import requests
from .config import url


def load_data(params: dict) -> dict | None:
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    print(f"Error: {response.status_code}")
    print(response.text)


if __name__ == "__main__":
    from config import params_iterator
    params = next(params_iterator)
    data = load_data(params)["data"]
    for flight in data:
        print(flight)
    # {'flight_date': '2025-04-07',
    # 'flight_status': 'scheduled',
    # 'departure': {
    #   'airport': 'Istanbul Airport',
    #   'timezone': 'Europe/Istanbul',
    #   'iata': 'IST',
    #   'icao': 'LTFM',
    #   'terminal': None,
    #   'gate': 'A4B',
    #   'delay': None,
    #   'scheduled': '2025-04-07T01:40:00+00:00',
    #   'estimated': '2025-04-07T01:40:00+00:00',
    #   'actual': None,
    #   'estimated_runway': None,
    #   'actual_runway': None
    # },
    # 'arrival': {
    #   'airport': 'Kuala Lumpur International Airport (klia)',
    #   'timezone': 'Asia/Kuala_Lumpur',
    #   'iata': 'KUL',
    #   'icao': 'WMKK',
    #   'terminal': '1',
    #   'gate': None,
    #   'baggage': None,
    #   'scheduled': '2025-04-07T17:05:00+00:00',
    #   'delay': None,
    #   'estimated': None,
    #   'actual': None,
    #   'estimated_runway': None,
    #   'actual_runway': None
    # },
    # 'airline': {
    #   'name': 'Malindo Air',
    #   'iata': 'OD',
    #   'icao': 'MXD'
    # },
    # 'flight': {
    #   'number': '9200',
    #   'iata': 'OD9200',
    #   'icao': 'MXD9200',
    #   'codeshared': {
    #       'airline_name': 'turkish airlines',
    #       'airline_iata': 'tk',
    #       'airline_icao': 'thy',
    #       'flight_number': '60',
    #       'flight_iata': 'tk60',
    #       'flight_icao': 'thy60'
    #    }
    #  },
    #  'aircraft': None,
    #  'live': None}