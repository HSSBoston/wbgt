import badger2040
from utils import displayWbgtInfo, displaySuggestions

LAT = 42.0
LON = -71.0
DEEP_SLEEP_INTERVAL = 1 # in minutes 

display = badger2040.Badger2040()
display.led(128)

if badger2040.pressed_to_wake(badger2040.BUTTON_DOWN):
    displaySuggestions(display)
elif badger2040.pressed_to_wake(badger2040.BUTTON_UP):
    displayWbgtInfo(display, LAT, LON, useWifi=False)
else:
    displayWbgtInfo(display, LAT, LON)

while True:
    if display.pressed(badger2040.BUTTON_DOWN):
        displaySuggestions(display)
    elif display.pressed(badger2040.BUTTON_UP):
        displayWbgtInfo(display, LAT, LON, useWifi=False)
    
    badger2040.sleep_for(DEEP_SLEEP_INTERVAL)
        # Set an RTC alert that will fire in DEEP_SLEEP_INTERVAL mins. 
        # Shut off power supply if the device is on battery.
        # Blocks until a button event or an RTC alert if the device is on USB power.
    