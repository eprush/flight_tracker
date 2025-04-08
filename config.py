import datetime

# Define your API token and the endpoint URL
API_TOKEN = 'beb8590873bff5b83d2972f1aee16234'
BASE_URL = 'https://api.aviationstack.com'
ENDPOINT = '/v1/flights'

# Construct the full URL
url = f"{BASE_URL}{ENDPOINT}"


# Define any query parameters, if needed (optional)
today = datetime.datetime.now()
# observe fon a hour
params_iterator = ( {
    "access_key": API_TOKEN,
    "date": today - datetime.timedelta(minutes=i)
    } for i in range(61)
)

#the Black Sea area
bounds = {
    "min_longitude": 27.77325,
    "max_longitude": 42.11512,
    "min_latitude": 40.8274,
    "max_latitude": 46.93029,
}

#Your PostgreSQL password (if you need to use this database)
password = "126768"
# All settings used to connect to the database
# user="postgres",
# password=password,
# host="127.0.0.1",
# port="5432"