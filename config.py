# Define your API token and the endpoint URL
API_TOKEN = 'your_api_token_here'
BASE_URL = 'https://fr24api.flightradar24.com/api'
ENDPOINT = '/live/flight-positions/light'

# Construct the full URL
url = f"{BASE_URL}{ENDPOINT}"

# Define the headers, including the Authorization header with your API token
headers = {
    'Accept': 'application/json',
    'Authorization':  f'Bearer {API_TOKEN}',
    'Accept-Version': 'v1'
}

# Define any query parameters, if needed (optional)
params = {
    'bounds': '50.682,46.218,14.422,22.243'  # Example coordinates
}