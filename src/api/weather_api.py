def fetch_weather_data(city):
    import requests
    from datetime import datetime
    from geopy.geocoders import Nominatim

    API_KEY = "your_actual_api_key_here"  # Replace with real key
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city)
    
    if not location:
        raise Exception("City not found!")

    lat = location.latitude
    lon = location.longitude
    date = datetime.now().strftime('%Y-%m-%d')

    url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={lon}&date={date}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if 'error' in data:
        raise Exception(data['error'])

    return data
