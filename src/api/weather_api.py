import requests
from datetime import datetime

WEATHER_API_KEY = "your_openweathermap_api_key"

def fetch_weather_summary(lat, lon, date=None):
    """
    Fetch daily weather summary from OpenWeather One Call 3.0 API.
    :param lat: Latitude
    :param lon: Longitude
    :param date: Date string in YYYY-MM-DD format (defaults to today)
    :return: Summary weather data or None
    """
    try:
        if date is None:
            date = datetime.today().strftime('%Y-%m-%d')

        url = (
            f"https://api.openweathermap.org/data/3.0/onecall/day_summary?"
            f"lat={lat}&lon={lon}&date={date}&appid={WEATHER_API_KEY}&units=metric"
        )

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        
        # Example of extracting some summary values — adjust based on your needs
        return {
            "date": date,
            "temp_max": data["temperature"]["maximum"],
            "temp_min": data["temperature"]["minimum"],
            "humidity": data["humidity"]["average"],
            "precipitation": data["precipitation"]["total"],
            "summary": data.get("summary", "No description available")
        }

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
