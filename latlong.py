from geopy.geocoders import Nominatim



api_key = "VGH2EXmyclRgyevMXbNcvtDEuZBvV2l4"

def get_lalong(loc:str):
    locator = Nominatim(user_agent = "plague",timeout = 10)
    location = locator.geocode(loc)
    
    if location:
        lat = location.latitude
        long = location.longitude
        return lat,long
    else:
        return None
 