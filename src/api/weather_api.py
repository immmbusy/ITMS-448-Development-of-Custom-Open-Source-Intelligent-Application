def fetch_weather_data(city):
    import requests
    from datetime import datetime
    from geopy.geocoders import Nominatim

    API_KEY = "9bec9e6444e7cf3de8ac3d384ff22c7a"
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city)
    
    if not location:
        raise Exception("City not found!")

    lat = location.latitude
    lon = location.longitude
    date = datetime.now().strftime('%Y-%m-%d')

    url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={lon}&date={date}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    data = response.json()
    print("Raw API Response:", data)  # Helps debug structure

    if 'temperature' not in data or 'humidity' not in data or 'wind' not in data:
        raise Exception("Expected weather keys not found in response.")

    # Extract real data (OpenWeather day_summary returns keys like this)
    standardized_data = {
        'name': city,
        'main': {
            'temp': data['temperature'].get('afternoon', 0),
            'humidity': data.get('humidity', 0),
            'pressure': data.get('pressure', 0)
        },
        'weather': [{
            'description': data.get('summary', {}).get('title', 'No summary available')
        }],
        'wind': {
            'speed': data['wind'].get('speed_avg', 0)
        }
    }

    return standardized_data
