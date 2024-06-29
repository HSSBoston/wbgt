from noaa_wbgt import getWbgt
import geocoder
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw

geoInfo = geocoder.ip("me")
lat = geoInfo.lat
lon = geoInfo.lng

currentWbgt, timeToWbgtDictToday, timeToWbgtDictTomorrow, timeToWbgtDictWeek = getWbgt(lat, lon)

print("Current WBGT (F): ", currentWbgt)
print(timeToWbgtDictToday)

maxWbgt = max(timeToWbgtDictToday.values())
#print(maxWbgt)

maxTime = []
maxTimeHr = []
for key,value in timeToWbgtDictToday.items():
    if value == maxWbgt:
        maxTime.append(key)

#print(maxTime)
for item in maxTime:
    Hr = int(item[11:13])
    if Hr > 12:
        Hr = str(Hr -12) + "PM"
    else:
        Hr = str(Hr) + "AM"
    maxTimeHr.append(Hr)
    
maxTimeHrStr = ""
if len(maxTimeHr) == 1:
    maxTimeHrStr = maxTimeHr[0]
else:
    maxTimeHrStr = maxTimeHr[0] + " ~ " + maxTimeHr[-1]

date = maxTime[0]
shortDate = date[5:10]

if maxWbgt > 86.2:
    condition = "Extreme"
elif maxWbgt > 84.2:
    condition = "High Risk"
elif maxWbgt > 81.1:
    condition = "Moderate Risk"
elif maxWbgt > 76.3:
    condition = "Less than Ideal"
else:
    condition = "Good conditions"

display = InkyPHAT("red")

image = Image.new("P", (display.WIDTH, display.HEIGHT), display.WHITE)
draw = ImageDraw.Draw(image)

# font = ImageFont.load_default()
fontBig = ImageFont.truetype("JetBrainsMono-Regular.ttf", 35)
fontSmall = ImageFont.truetype("JetBrainsMono-Regular.ttf", 25)
fontSmaller = ImageFont.truetype("JetBrainsMono-Regular.ttf", 20)

draw.text((0,0), "WBGT" + " " + shortDate, display.BLACK, font=fontSmaller)
draw.text((0, 25), str(maxWbgt) + "F ", display.RED, font=fontBig)
draw.text((70, 30), maxTimeHrStr , display.BLACK, font=fontSmall)
draw.text((0, 70), condition, display.RED, font=fontSmaller)

display.set_image(image)
display.show()



