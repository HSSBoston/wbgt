import geocoder
from noaa_wbgt import getWbgt
from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw

regionCategory = 1 

fontBig =     ImageFont.truetype("JetBrainsMono-Regular.ttf", 35)
fontSmall =   ImageFont.truetype("JetBrainsMono-Regular.ttf", 25)
fontSmaller = ImageFont.truetype("JetBrainsMono-Regular.ttf", 20)

def getLatLon(): 
    geoInfo = geocoder.ip("me")
    return (geoInfo.lat, geoInfo.lng)
    
def getAlertCondition(wbgt, regionCategory):
    assert regionCategory in [1, 2, 3], "Invalid region number: " +\
           str(regionCategory) + "." + " It must be 1, 2 or 3."

    if regionCategory == 1:
        if   wbgt > 86.1: condition = "Extreme"
        elif wbgt > 84.1: condition = "High Risk"
        elif wbgt > 81.0: condition = "Moderate Risk"
        elif wbgt > 76.1: condition = "Less than Ideal"
        else:             condition = "Good conditions"
    elif regionCategory == 2:
        if   wbgt > 89.7: condition = "Extreme"
        elif wbgt > 87.7: condition = "High Risk"
        elif wbgt > 84.6: condition = "Moderate Risk"
        elif wbgt > 79.8: condition = "Less than Ideal"
        else:             condition = "Good conditions"
    elif regionCategory == 3:
        if   wbgt > 91.9:   condition = "Extreme"
        elif wbgt > 90.0: condition = "High Risk"
        elif wbgt > 87.0: condition = "Moderate Risk"
        elif wbgt > 82.1: condition = "Less than Ideal"
        else:             condition = "Good conditions"
    return condition

def maxWbgtHrToHrDuration(maxWbgt):
    maxTime = []
    for key, value in timeToWbgtDictToday.items():
        if value == maxWbgt:
            maxTime.append(key)

    date = maxTime[0]
    shortDate = date[5:10]

    maxTimeHr = []
    for item in maxTime:
        Hr = int(item[11:13])
        if Hr > 12: Hr = str(Hr - 12) + "PM"
        else:       Hr = str(Hr)      + "AM"
        maxTimeHr.append(Hr)
        
    maxTimeHrStr = ""
    if len(maxTimeHr) == 1:
        maxTimeHrStr = maxTimeHr[0]
    else:
        maxTimeHrStr = maxTimeHr[0] + " ~ " + maxTimeHr[-1]
    return (shortDate, maxTimeHrStr)

def displayWbgtInfo(date, maxWbgt, maxWbgtHrToHrDuration, alertCondition):
    display = InkyPHAT("red")
    image = Image.new("P", (display.WIDTH, display.HEIGHT), display.WHITE)
    draw = ImageDraw.Draw(image)

    draw.text((0,0),   "WBGT" + " " + date,    display.BLACK, font=fontSmaller)
    draw.text((0, 25),  str(maxWbgt) + "F ",   display.RED,   font=fontBig)
    draw.text((70, 30), maxWbgtHrToHrDuration, display.BLACK, font=fontSmall)
    draw.text((0, 70),  alertCondition,        display.RED,   font=fontSmaller)
    
    display.set_image(image)
    display.show()


lat, lon = getLatLon()
currentWbgt, timeToWbgtDictToday, timeToWbgtDictTomorrow, timeToWbgtDictWeek = getWbgt(lat, lon)

maxWbgt = max(timeToWbgtDictToday.values())
todayDate, hrToHr = maxWbgtHrToHrDuration(maxWbgt)
alertCond = getAlertCondition(maxWbgt, regionCategory)

displayWbgtInfo(todayDate, maxWbgt, hrToHr, alertCond)
