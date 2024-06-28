from openweather import *

weatherApiKey = "7d5ad812ef8968d100698dd2920efc8b" 

cityName = "Boston"
stateCode = "MA"
weatherData = getUsWeather(cityName, stateCode, weatherApiKey, unit="imperial")
temp, feelsLike, humidity = getCurrentTempHumidity(weatherData)
print(cityName + ", " + stateCode)
print("Temp (C): " + str(temp) + ", Feels like (C): " + str(feelsLike) + \
      ", Humidity (%): " + str(humidity))
print("----------")


main, description, iconId = getCurrentWeatherCondition(weatherData)
print(main, description, iconId)
