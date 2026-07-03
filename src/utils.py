from geopy import Nominatim

def get_coords(city):
    geolocator = Nominatim(user_agent='etl_weather_service')

    location = geolocator.geocode(city)

    if location:
        return (location.latitude, location.longitude)
    return None