# Library to download WBGT (Web Bulb Globe Temperature) forecasts with
# National Digital Forecast Database (NDFD).
#
# June 13, 2025, v0.04
#
# NDFD is developed by Meteorological Development Laboratory (MDL) of
# NOAA (National Oceanic and Atmospheric Administration) for
# National Weather Service (NWS).
#   https://vlab.noaa.gov/web/mdl/home
#   https://vlab.noaa.gov/web/mdl/ndfd
#
# This library accesses to NDFD data via REST in XML (Digital Weather
# Markup Language (DWML).
#   https://digital.weather.gov/xml/rest.php
# The list of weather query parameters: 
#  https://digital.weather.gov/xml/docs/elementInputNames.php
#
# To use this library, install the requests and xmltodict modules: 
#   pip3 install requests
#   pip3 install xmltodict

import requests, xmltodict
from datetime import datetime, timedelta
from pprint import pprint

def downloadWbgt(lat, lon):
    dtNow = datetime.now().replace(microsecond=0).isoformat()
    url = "https://digital.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?" +\
          "&XMLformat=DWML" +\
          "&lat=" + str(lat) +\
          "&lon=" + str(lon) +\
          "&product=time-series" +\
          "&begin=" + dtNow +\
          "&end=" + "" +\
          "&Unit=e" +\
          "&wbgt=wbgt"
    # When "end=" is omitted in the URL, a 1-week forecast is returned. 
    # "&begin={{now().replace(microsecond=0).isoformat()}}" +\
    # "&end={{(now()+timedelta(hours=1)).replace(microsecond=0).isoformat()}}" +\

    response = requests.get(url)
    if response.status_code == 200:
        responseDict = xmltodict.parse(response.text)
        return responseDict
    else:
        raise RuntimeError("Request failed. Status code: " + str(response.status_code))

def getWbgt(lat, lon):
    dtNow = datetime.now()
    dtNowIso = dtNow.isoformat()
    today = dtNowIso.split("T")[0]
    
    dtTomorrow = dtNow + timedelta(days=1)
    dtTomorrowIso = dtTomorrow.isoformat()
    tomorrow = dtTomorrowIso.split("T")[0]
#     print(today, tomorrow)
    
    responseDict = downloadWbgt(lat, lon)
    wbgtVals = responseDict["dwml"]["data"]["parameters"]["temperature"]["value"]
    timeStamps = responseDict["dwml"]["data"]["time-layout"]["start-valid-time"]
    currentWbgt = int(wbgtVals[0])
    
    timeToWbgtDictToday = {}
    timeToWbgtDictTomorrow ={}
    timeToWbgtDictWeek = {}
    
    for i in range(len(timeStamps)):
        tStamp = timeStamps[i]
        wbgt = wbgtVals[i]
        timeToWbgtDictWeek[tStamp] = int(wbgt)
        if tStamp.startswith(today):
            timeToWbgtDictToday[tStamp] = int(wbgt)
        if tStamp.startswith(tomorrow):
            timeToWbgtDictTomorrow[tStamp] = int(wbgt)
    return currentWbgt, timeToWbgtDictToday, timeToWbgtDictTomorrow, timeToWbgtDictWeek

def getWbgtSummary(lat, lon):
    currentWbgt, timeToWbgtDictToday, timeToWbgtDictTomorrow, timeToWbgtDictWeek = getWbgt(lat, lon)

    todayMax = max(timeToWbgtDictToday.values())
    todayMin = min(timeToWbgtDictToday.values())
    tomorrowMax = max(timeToWbgtDictTomorrow.values())
    tomorrowMin = min(timeToWbgtDictTomorrow.values())
    weekMax = max(timeToWbgtDictWeek.values())
    weekMin = min(timeToWbgtDictWeek.values())
    return currentWbgt, todayMax, todayMin, tomorrowMax, tomorrowMin, weekMax, weekMin
    
if __name__ == "__main__":    
    lat = 42.0
    lon = -71.0
#     pprint( downloadWbgt(lat, lon) )
    print("currentWbgt, todayMax, todayMin, tomorrowMax, tomorrowMin, weekMax, weekMin")
    print( getWbgtSummary(lat, lon) )

