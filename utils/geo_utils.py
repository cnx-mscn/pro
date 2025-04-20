
from geopy.geocoders import Nominatim

def get_coordinates(city):
    geo = Nominatim(user_agent="montaj_app")
    loc = geo.geocode(city)
    if loc:
        return loc.latitude, loc.longitude
    return 39.0, 35.0
