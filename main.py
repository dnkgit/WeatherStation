from display_func import DISP_CONTROL
from time_ext import TIME_EXT
from data_conditioning import SENSOR_DATA
from micropython import const
from adafruit_io_req import AdafruitIO
import ws_wlan
from time import sleep
from rtc import REALTIMECLOCK
import my_secrets

_VERSION        	= const(100)
_SM_INIT			= const(0)
_SM_DO_CONNECT		= const(1)
_SM_DO_NTP			= const(2)
_SM_RUNNING			= const(3)
_SM_RESYNC_NTP		= const(4)
_SM_RECONNECT		= const(5)

def UpdateDisplay():
    global toggleDone

    d.setDispSetLine(0, 0, td.getCurrentTimeAsString())
    d.setDispSetLine(0, 1, td.getTimeDateString())
    d.setDispSetLine(0, 2, str(td.get_totalUptimeSecs()))
    d.setDispSetLine(0, 3, "xxx.xxx.xxx.xxx")
    d.setDispSetLine(0, 4, "RC: 0")
    
    d.setDispSetLine(1, 0, td.getCurrentTimeAsString())
    d.setDispSetLine(1, 1, str(counter))
    d.setDispSetLine(1, 2, td.get_totalUptimeString())
    d.setDispSetLine(1, 3, f"{sd.getTemp_DegC():2.02f}C {sd.getHumidity_pc():2.02f}%")
    d.setDispSetLine(1, 4, f"{sd.getPressure_hPa():4.02f}hPa")
    d.runDisplay()

    if (td.getSeconds() % 3) == 0:
        if toggleDone == False:
            d.toggleFrameBuffer()
            toggleDone = True
    else:
        toggleDone = False

rtc = REALTIMECLOCK()
d = DISP_CONTROL()
td = TIME_EXT()
sd = SENSOR_DATA(samplePeriods=0)
#af = AdafruitIO(aio_username=my_secrets.ADAFRUIT_ID, aio_key=my_secrets.ADAFRUIT_KEY)
wl = ws_wlan.WS_WLAN(debugRequired=True)

smStateVariable = _SM_INIT
counter = 0
toggleDone = False

while True:

    td.updateUptime()

    if smStateVariable == _SM_INIT:
        
        d.setDispSetLine(0, 0, f"{smStateVariable} _SM_INIT")
        d.setDispSetLine(0, 1, "")
        d.setDispSetLine(0, 2, "")
        d.setDispSetLine(0, 3, "")
        d.setDispSetLine(0, 4, "")
        d.runDisplay()

        # Configure WIFI
        wl.set_SSID(my_secrets.WIFI_ID)
        wl.set_WPA2_Password(my_secrets.WIFI_PASS)
        wl.setStateMachineState(ws_wlan.WLAN_STATE_INIT)
        
        smStateVariable = _SM_DO_CONNECT

    elif smStateVariable == _SM_DO_CONNECT:

        wl.runStateMachine()

        d.setDispSetLine(0, 0, f"{smStateVariable} _SM_DO_CONNECT")
        d.setDispSetLine(0, 1, f"WLAN {wl.getStateMachineState()}")
        d.setDispSetLine(0, 2, "")
        d.setDispSetLine(0, 3, "")
        d.setDispSetLine(0, 4, "")
        d.runDisplay()

        if wl.getStateMachineState() == ws_wlan.WLAN_STATE_CONNECTED:
            d.setDispSetLine(0, 1, f"WLAN {wl.getStateMachineState()}")
            d.setDispSetLine(0, 2, f"{wl.get_WLAN_ipaddress()}")
            d.setDispSetLine(0, 3, f"{wl.get_WLAN_ipgateway()}")
            d.runDisplay()
    
            smStateVariable = _SM_DO_NTP  
        
    elif smStateVariable == _SM_DO_NTP:

        wl.runStateMachine()

        rtc.syncNtpTime()
        
        d.setDispSetLine(0, 0, f"{smStateVariable} _SM_DO_NTP")
        d.setDispSetLine(0, 1, f"{td.getTimeDateString()}")
        d.runDisplay()
        
        smStateVariable = _SM_RUNNING

    elif smStateVariable == _SM_RUNNING:

        d.setDispSetLine(0, 0, f"{smStateVariable} _SM_RUNNING")
        d.setDispSetLine(0, 1, f"{td.getTimeDateString()}")
        d.runDisplay()
        
        sd.updateValues()

    elif smStateVariable == _SM_RESYNC_NTP:

        pass

    elif smStateVariable == _SM_RECONNECT:
    
        pass
        
    else:
        smStateVariable = _SM_INIT
    

    counter += 1


'''
    sd.updateValues()
    td.updateUptime()
    
    insTemp = sd.getTemp_DegC()
    insPres = sd.getPressure_hPa()
    insHumd = sd.getHumidity_pc()

    if td.isNewSecond() == True:
        firstData = True
        sd.updateSecondValuesAll()
        avgTemp = sd.getAverageTempStr(10)
        avgPres = sd.getAveragePressureStr(10)
        avgHumd = sd.getAverageHumidityStr(10)

        if (td.getSeconds() % 30) == 0:
            print(avgTemp)
            if wl.getStateMachineState() == ws_wlan.WLAN_STATE_CONNECTED :
                af.sendDatapoint('bme280-tempdegc', avgTemp)
                af.sendDatapoint('bme280-pressure-hpa', avgPres)
                af.sendDatapoint('bme280-humidityperc', avgHumd)
            else:
                print("No connection.")

        if (td.get_totalUptimeSecs() % 60) == 0:
            print(f"Uptime {td.get_totalUptimeSecs()}")

    if firstData:
        d.setLine(line=0, newString=td.getTimeDateString())
        d.setLine(line=1, newString=f"{insTemp:.2f} {avgTemp} C")
        d.setLine(line=2, newString=f"{insPres:.2f} {avgPres}")
        d.setLine(line=3, newString=f"{insHumd:.2f} {avgHumd} %")
        d.showLines()

    sleep(0.1)
'''