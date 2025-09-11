# Library to download WBGT (Web Bulb Globe Temperature) forecasts with
# National Digital Forecast Database (NDFD) with MicroPython
#
# June 15, 2025, v0.01
#
# NDFD is developed by Meteorological Development Laboratory (MDL) of
# NOAA (National Oceanic and Atmospheric Administration) for
# National Weather Service (NWS).
#   https://vlab.noaa.gov/web/mdl/home
#   https://vlab.noaa.gov/web/mdl/ndfd
#
# This library accesses NDFD data in XML (Digital Weather
# Markup Language (DWML) via REST:
#   https://digital.weather.gov/xml/rest.php
# The list of weather query parameters: 
#  https://digital.weather.gov/xml/docs/elementInputNames.php
#
# This library requires the urequests module.

import badger2040, urequests

# Takes lat and lon in string.
# Returns timestamp and wbgt forecast in string.
#
def downloadWbgt(lat, lon):
    url = "https://digital.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?" +\
          "&XMLformat=DWML" +\
          "&lat=" + str(lat) +\
          "&lon=" + str(lon) +\
          "&product=time-series" +\
          "&begin=" + "" +\
          "&end=" + "" +\
          "&Unit=e" +\
          "&wbgt=wbgt"
    # "&begin=" + dtNow +\
    # When "end=" is omitted in the URL, a 1-week forecast is returned. 
    # "&begin={{now().replace(microsecond=0).isoformat()}}" +\
    # "&end={{(now()+timedelta(hours=1)).replace(microsecond=0).isoformat()}}" +\

    response = urequests.get(url)
    if response.status_code == 200:
        responseStr = (response.text).splitlines()
        for line in responseStr:
            if "<creation-date" in line:
                timeStamp = line[line.find(">")+1 : line.find("/")-1]
                break
        for line in responseStr:
            if "<value>" in line:
                wbgt = line.strip().replace("<value>", "").replace("</value>", "")
                break
        return (timeStamp, wbgt)
    else:
        raise RuntimeError("Request failed. Status code: " + str(response.status_code))
    
if __name__ == "__main__":    
    lat = 42.36
    lon = -71.01

    display = badger2040.Badger2040()
    # Connects to the wireless network. Make sure to complete WIFI_CONFIG.py.
    display.connect()
    timeStamp, wbgt = downloadWbgt(lat, lon)
    print("Timestamp (UTC):" , timeStamp)
    print("WBGT forecast:", wbgt)
    

