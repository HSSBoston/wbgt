import badger2040
from badger2040 import WIDTH, HEIGHT
from unoaa_wbgt import downloadWbgt
wbgt = 0
condition = "a"

def getWbgt(lat, lon):
    timeStamp, wbgt = downloadWbgt(lat, lon)
    
    date = timeStamp.split("T")[0][5:]
    time = timeStamp.split("T")[1][:5]
    if int(time[:2])<12:
        time = time + " AM"
    else:
        time = time.replace(time[:2], str(int(time[:2])-16), 1) + " PM"
    return (date, time, int(wbgt))

def displayWbgtInfo(display, lat, lon, useWifi=True):
    if useWifi:       
        # Connects to the wireless network. Make sure to complete WIFI_CONFIG.py.
        display.connect()
        date, time, wbgt = getWbgt(lat, lon)
        with open("wbgt.txt", "w") as f:
            f.write(date + "\n" + time + "\n" + str(wbgt))
    else:
        try:
            with open("wbgt.txt") as f:
                date = f.readline()
                time = f.readline()
                wbgt = int(f.readline())
        except OSError:
            date = "00-00"
            time = "00:00"
            wbgt = 0

    # Clear to white
    display.set_pen(15)
    display.clear()
    display.set_font("bitmap8")
    
    # upper black rectangle
    display.set_pen(0)
    upperRecHeight = int(HEIGHT/6)
    display.rectangle(0, 0, WIDTH, upperRecHeight)

    # date and "WBGT"
    display.set_pen(15)
    display.text(date, 5, 5, scale=2)
    display.text("WBGT", display.measure_text(date)+15, 5, scale=2)

    # last update time
    display.set_pen(0)
    display.text(time, 20, upperRecHeight+5, scale=3)

    # wbgt number
    display.text(str(wbgt), 20, upperRecHeight+24+20, scale=7)
    
    # condition
    condition = wbgtCondition(wbgt)
    display.text(condition, int(WIDTH/2), int(HEIGHT/2), scale=3)

    display.update()
    
def wbgtCondition(wbgt):
    if wbgt <= 76:
        condition = "Good"
    elif 76.1 <= wbgt <= 81:
        condition = "Cautious"
    elif 81.1 <= wbgt <=84:
        condition = "Risky"
    elif 84.1 <= wbgt <=86:
        condition = "High Risk"
    else:
        condition = "Extreme"

    return condition

def displaySuggestions(display):
    # Clear to white
    condition = wbgtCondition(wbgt)
    display.set_pen(15)
    display.clear()
    display.set_font("bitmap8")
    
    display.set_pen(0)
    display.text(condition+":\n", 5, 5, wordwrap=int(WIDTH),scale=3)
    #"Normal Activites. At least 3 seperate 3-min breaks each hr."
    if condition=="Good":
        display.text("Normal Activites. At least 3 seperate 3-min breaks each hr.", 0, 39,wordwrap=296, scale=2)
    elif condition=="Fine":
        display.text("Use discreation for intese or long exercise. At least 3 seperate 4-min breaks each hr.",0, 39,wordwrap=296,scale=2)
    elif condition=="Poor":
        display.text("Be alert. Max 2 hrs of practice. 4 seperate 4-min breaks each hr.",0,39,wordwrap=296,scale=2)
    elif condition=="High Risk":
        display.text("Be extremely cautious. Max 1 hr of practice. No conditioning activities. 20-min breaks distributes throughout the hr.",0,39,wordwrap=296,scale=2)
    else:
        display.text("No outdoor workouts. Delay practice/events until a cooler WBGT is reached.",0,39,wordwrap=296,scale=2)

    display.update()