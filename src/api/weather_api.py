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

    # OpenWeather API OneCall endpoint for current weather
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    data = response.json()
    print("Raw API Response:", data)  # Helps debug structure

    # Check if expected data exists in the response
    if 'current' not in data or 'weather' not in data['current']:
        raise Exception("Expected weather data not found in response.")

    # Extract relevant data
    current_weather = data['current']
    standardized_data = {
        'name': city,
        'main': {
            'temp': current_weather.get('temp', 0),
            'humidity': current_weather.get('humidity', 0),
            'pressure': current_weather.get('pressure', 0)
        },
        'weather': [{
            'description': current_weather['weather'][0].get('description', 'No description available')
        }],
        'wind': {
            'speed': current_weather.get('wind_speed', 0)
        }
    }

    return standardized_data
