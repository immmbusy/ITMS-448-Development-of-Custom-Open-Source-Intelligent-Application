import requests

WEATHER_API_KEY = "your_openweathermap_api_key"

def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data.get("cod") != 200:
        raise Exception(data.get("message", "Failed to fetch weather!"))
    
    return data
