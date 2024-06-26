from noaa_wbgt import getWbgtSummary

lat = 42.490027972375344
lon = -71.28465073182961

currentWbgt, todayMax, todayMin, tomorrowMax, tomorrowMin, weekMax, weekMin = getWbgtSummary(lat, lon)

print("Current WBGT (F): ", currentWbgt)
print("Max WBGT today (F): ", todayMax)
print("Min WBGT today (F): ", todayMin)
print("Max WBGT tomorrow (F): ", tomorrowMax)
print("Min WBGT tomorrow (F): ", tomorrowMin)
