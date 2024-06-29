# Library to access and use OpenWeatherMap API
# June 27, 2024 v0.06
# IoT for Kids: https://jxsboston.github.io/IoT-Kids/
#
# OpenWeatherMap API: https://openweathermap.org/api
# Free tier APIs: https://openweathermap.org/price

# This library uses OpenWeather's One Call API 1.0 and
# Geocoding API:
#   https://openweathermap.org/api/one-call-api
#   https://openweathermap.org/api/geocoding-api
# OpenWeather's Geocoding API uses ISO 3166 country code:
#   https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
# As for weather conditions ("main" and "description"), see:
#   https://openweathermap.org/weather-conditions

import requests, json
from typing import Tuple
from PIL import Image
from io import BytesIO
# from geopy.geocoders import Nominatim
# 
# nominatimAppName = "iot" + os.uname()[1]
# geolocator = Nominatim(user_agent=nominatimAppName)

#
# Response data format: https://openweathermap.org/current
# 
def getLatLonWeather(lat, lon, apiKey, unit="imperial"):
    url = "https://api.openweathermap.org/data/2.5/weather?" +\
              "lat=" + str(lat) + "&lon=" + str(lon) + \
              "&appid=" + apiKey +\
              "&units=" + unit
    response = requests.get(url)
    if response.status_code == 200:
        return response
    else:
        raise RuntimeError("OpenWeather Response Error: " + response.text)

#               "&exclude=minutely,hourly" + \


def getUsWeather(cityName, stateCode, apiKey, unit="imperial"):
    lat, lon = getUsLatLon(cityName, stateCode, apiKey)
    if lat is not None or lon is not None: 
        return getLatLonWeather(lat, lon, apiKey, unit)
    else:
        print("Geocoding failed: Invalid Lat/lon.")
        return None
        

def getIntlWeather(cityName, countryCode, apiKey, unit="imperial"):
    lat, lon = getIntlLatLon(cityName, countryCode, apiKey)
    if lat is not None or lon is not None: 
        return getLatLonWeather(lat, lon, apiKey, unit)
    else:
        print("Geocoding failed: Invalid Lat/lon.")
        return None

def getZipWeather(zipCode, countryCode, apiKey, unit="imperial"):
    lat, lon = getZipLatLon(zipCode, countryCode, apiKey)
    if lat is not None or lon is not None: 
        return getLatLonWeather(lat, lon, apiKey, unit)
    else:
        print("Geocoding failed: Invalid Lat/lon.")
        return None

# Extract the current air temp, feels-like temp and humidity from an OpenWeatherMap
# response message and return them as a tuple. 
# 
def getCurrentTempHumidity(response: requests.Response) -> Tuple[float, float, int]:
    assert response != None, "OpenWeather response data is invalid (==None)."
    responseDict = json.loads(response.text)
    if "main" in responseDict:
        temp = responseDict["main"]["temp"]
        feelsLike = responseDict["main"]["feels_like"]
        humidity = responseDict["main"]["humidity"]
        return (temp, feelsLike, humidity)
    else:
        raise RuntimeError("OpenWeather response is invalid. It doesn't have the main key.")



def getCurrentWind(response: requests.Response) -> Tuple[float, float, float]:
    assert response != None, "OpenWeather response data is invalid (==None)."
    responseDict = json.loads(response.text)
    if "wind" in responseDict:        
        windDict = responseDict["wind"]
        if "speed" in windDict:
            windSpeed = windDict["speed"]
        else:
            windSpeed = None
        if "deg" in windDict:
            windDeg = windDict["deg"]
        else:
            windDeg = None
        if "gust" in windDict:
            windGust = windDict["gust"]
        else:
            windGust = None
        return (windSpeed, windDeg, windGust)
    else:
        raise RuntimeError("OpenWeather response is invalid. It doesn't have the wind key.")

def getCurrentWeatherCondition(response: requests.Response) -> Tuple[str, str, str]:
    assert response != None, "OpenWeather response data is invalid (==None)."
    responseDict = json.loads(response.text)
    if "weather" in responseDict:
        weatherCondDict = responseDict["weather"][0]
        main = weatherCondDict["main"]
        description = weatherCondDict["description"]
        iconId = weatherCondDict["icon"]
        return (main, description, iconId)
    else:
        raise RuntimeError("OpenWeather response is invalid. It doesn't have the weather key.")

def getCurrentAtmosphericPressure(response: requests.Response) -> int:
    assert response != None, "OpenWeather response data is invalid (==None)."
    responseDict = json.loads(response.text)
    if "main" in responseDict:
        mainDict = responseDict["main"]
        if "pressure" in mainDict:
            return mainDict["pressure"]
        else:
            return None
    else:
        raise RuntimeError("OpenWeather response is invalid. It doesn't have the main key.")


def getCurrentCloudiness(response: requests.Response) -> int:
    assert response != None, "OpenWeather response data is invalid (==None)."
    responseDict = json.loads(response.text)
    if "clouds" in responseDict:
        return responseDict["clouds"]["all"]
    else:
        raise RuntimeError("OpenWeather response is invalid. It doesn't have the clouds key.")

def getCurrentRain(response):
    if response.status_code == 200:
        responseDict = json.loads(response.text)
        if "current" in responseDict:
            currentDict = responseDict["current"]
            if "rain" in currentDict:
                rainDict = currentDict["rain"]
                rain1h = rainDict["rain.1h"]
                return rain1h
            else:
                return None
        else:
            return None
    else:
        print("OpenWeather Response Error. Status code: " + str(response.status_code))
        return None

def getCurrentSnow(response): 
    if response.status_code == 200:
        responseDict = json.loads(response.text)
        if "current" in responseDict:
            currentDict = responseDict["current"]
            if "snow" in currentDict:
                rainDict = currentDict["snow"]
                snow1h = rainDict["snow.1h"]
                return snow1h
            else:
                return None
        else:
            return None
    else:
        print("OpenWeather Response Error. Status code: " + str(response.status_code))
        return None

def getWeatherIconImage(iconId, size):
    if iconId == None:
        return None
    if size != "2x" and size != "4x":
        return None
    url = "http://openweathermap.org/img/wn/" + \
              iconId + "@" + size +".png"
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        if image != None:
            return image
        else:
            print("Donwnloaded icon not valid.")
            return None
    else:
        print("OpenWeather Response Error. Status code: " + str(response.status_code))
        return None
        

def getTempHumidityToday(response):
    return getTempHumidityForecast(response, 0)

def getTempHumidityTomorrow(response):
    return getTempHumidityForecast(response, 1)

def getTempHumidityForecast(response, daysLater):
    if response == None:
        return (None, None, None, None)
    if response.status_code == 200:
        responseDict = json.loads(response.text)
        if "daily" in responseDict:
            forecast = responseDict["daily"][daysLater]
            dayTemp = forecast["temp"]["day"]
            minTemp = forecast["temp"]["min"]
            maxTemp = forecast["temp"]["max"]
            humidity = forecast["humidity"]
            return (dayTemp, minTemp, maxTemp, humidity)
        else:
            return (None, None, None, None)
    else:
        print("OpenWeather Response Error. Status code: " + str(response.status_code))
        return (None, None, None, None)

def getFeelsLikeToday(response):
    return getFeelsLikeForecast(response, 0)

def getFeelsLikeTomorrow(response):
    return getFeelsLikeForecast(response, 1)

def getFeelsLikeForecast(response, daysLater):
    if response == None:
        return (None, None, None, None)
    if response.status_code == 200:
        responseDict = json.loads(response.text)
        if "daily" in responseDict:
            forecast = responseDict["daily"][daysLater]
            morningTemp = forecast["feels_like"]["morn"]
            dayTemp = forecast["feels_like"]["day"]
            eveTemp = forecast["feels_like"]["eve"]
            nightTemp = forecast["feels_like"]["night"]
            return (morningTemp, dayTemp, eveTemp, nightTemp)
        else:
            return (None, None, None, None)
    else:
        print("OpenWeather Response Error. Status code: " + str(response.status_code))
        return (None, None, None, None)

def getWeatherConditionToday(response):
    return getWeatherConditionForecast(response, 0)

def getWeatherConditionTomorrow(response):
    return getWeatherConditionForecast(response, 1)

def getWeatherConditionForecast(response, daysLater):
    if response == None:
        return (None, None, None)
    if response.status_code == 200:
        responseDict = json.loads(response.text)
        if "daily" in responseDict:
            forecast = responseDict["daily"][daysLater]
            weather = forecast["weather"][0]
            main = weather["main"]
            description = weather["description"]
            iconId = weather["icon"]
            return (main, description, iconId)
        else:
            return (None, None, None)
    else:
        print("OpenWeather Response Error. Status code: " + str(response.status_code))
        return (None, None, None)

def getCloudinessToday(response):
    return getCloudinessForecast(response, 0)

def getCloudinessTomorrow(response):
    return getCloudinessForecast(response, 1)

def getCloudinessForecast(response, daysLater):
    if response == None:
        return None
    if daysLater > 5:
        return None
    if response.status_code == 200:
        responseDict = json.loads(response.text)
        if "daily" in responseDict:
            forecast = responseDict["daily"][daysLater]
            cloudiness = forecast["clouds"]
            return cloudiness
        else:
            return None
    else:
        print("OpenWeather Response Error. Status code: " + str(response.status_code))
        return None


def getUsLatLon(cityName, stateCode, apiKey):
    url = "http://api.openweathermap.org/geo/1.0/direct?q=" + \
              cityName + "," + stateCode + "," + "US" + \
              "&appid=" + apiKey
    return getLatLon(url)

def getIntlLatLon(cityName, countryCode, apiKey):
    url = "http://api.openweathermap.org/geo/1.0/direct?q=" + \
              cityName + ",," + countryCode + \
              "&appid=" + apiKey
    return getLatLon(url)

def getZipLatLon(zipCode, countryCode, apiKey):
    url = "http://api.openweathermap.org/geo/1.0/zip?zip=" + \
              zipCode + "," + countryCode + \
              "&appid=" + apiKey
    response = requests.get(url)
    if response.status_code == 200:
        responseDict = json.loads(response.text)
        if "lat" in responseDict and "lon" in responseDict:
            lat = responseDict["lat"]
            lon = responseDict["lon"]
            return (lat, lon)
        else:
            print("OpenWeather Response Invalid: Lat/Lon Not Available.")
            return (None, None)
    else:
        print("OpenWeather Response Error. Status code: " + str(response.status_code))
        return (None, None)

def getLatLon(url):
    response = requests.get(url)
    if response.status_code == 200:
        responseList = json.loads(response.text)
        firstResponse = responseList[0]
        if "lat" in firstResponse and "lon" in firstResponse:
            lat = firstResponse["lat"]
            lon = firstResponse["lon"]
            return (lat, lon)
        else:
            print("OpenWeather Response Invalid: Lat/Lon Not Available.")
            return (None, None)
    else:
        print("OpenWeather Response Error. Status code: " + str(response.status_code))
        return (None, None)

# def getCurrentUvi(response): 
#     if response == None:
#         return None
#     if response.status_code == 200:
#         responseDict = json.loads(response.text)
#         if "current" in responseDict:
#             currentDict = responseDict["current"]
#             if "uvi" in currentDict:
#                 return currentDict["uvi"]
#             else:
#                 return None
#         else:
#             return None
#     else:
#         print("OpenWeather Response Error. Status code: " + str(response.status_code))
#         return None

# def getUsCityWeather(cityName, stateCode, unit, apiKey):
#     structuredQuery = {"city" : cityName,
#                        "state" : stateCode,
#                        "country" : "United States"}
#     location = geolocator.geocode(query=structuredQuery)
#     locationDataset = location.raw
#     return getLatLonWeather(locationDataset["lat"], locationDataset["lon"], unit, apiKey)
# 
# 
# def getUsTownWeather(townName, stateCode, unit, apiKey):
#     structuredQuery = {"town" : townName,
#                        "state" : stateCode,
#                        "country" : "United States"}
#     location = geolocator.geocode(query=structuredQuery)
#     locationDataset = location.raw
#     return getLatLonWeather(locationDataset["lat"], locationDataset["lon"], unit, apiKey)
# 
# def getIntlCityWeather(cityName, countryCode, unit, apiKey):
#     structuredQuery = {"city" : cityName,
#                        "country" : countryCode}
#     location = geolocator.geocode(query=structuredQuery)
#     locationDataset = location.raw
#     return getLatLonWeather(locationDataset["lat"], locationDataset["lon"], unit, apiKey)
