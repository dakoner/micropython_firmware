# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(0)
import network

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.connect('artdeco', 'Recurser')
try:
    wlan.config(pm=wlan.PM_NONE)
except AttributeError:
    print("Wifi powersave not supported in this firmware")

print(wlan.ifconfig())         # get the interface's IP/netmask/gw/DNS addresses

import webrepl

try:
    webrepl.start()
except:
    print("failed to start webrepl")
