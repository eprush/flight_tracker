import datetime

# Define your API token and the endpoint URL
API_TOKEN = 'beb8590873bff5b83d2972f1aee16234'
BASE_URL = 'https://api.aviationstack.com'
ENDPOINT = '/v1/flights'

# Construct the full URL
url = f"{BASE_URL}{ENDPOINT}"


# Define any query parameters, if needed (optional)
params = {
    "access_key": API_TOKEN  # Example coordinates
}

#the Black Sea area
bounds = {
    "min_longitude": 27.77325,
    "max_longitude": 42.11512,
    "min_latitude": 40.8274,
    "max_latitude": 46.93029,
}