from openweather import *
from PIL import Image

weatherApiKey = "7d5ad812ef8968d100698dd2920efc8b" 

latitude = 42.3663
longitude = -71.0095

weatherData = getLatLonWeather(latitude, longitude, weatherApiKey, unit="imperial")

temp, feelsLike, humidity = getCurrentTempHumidity(weatherData)

print("Temp (C): " + str(temp) + ", Feels like (C): " + str(feelsLike) + \
      ", Humidity (%): " + str(humidity))
print("----------")


main, description, iconId = getCurrentWeatherCondition(weatherData)
print(main, description, iconId)

weatherImg = getWeatherIconImage(iconId, "4x")
