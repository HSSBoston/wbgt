import geocoder
from usstates import *

geoInfo = geocoder.ip("me")
ip = geoInfo.ip
lat = geoInfo.lat
lon = geoInfo.lng
city = geoInfo.city
state = geoInfo.state
zipCode = geoInfo.postal
country = geoInfo.country

print(ip, lat, lon, city, state, zipCode, country)

stateCode = stateToStateCode[state]
print(stateCode)
