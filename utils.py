import requests
from config import API_KEY_WEATHER

def fetch_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY_WEATHER}&q={city}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    elif response.status_code == 404:
        return {"error": "City not found"}
    else:
        return {"error": "Failed to fetch weather"}