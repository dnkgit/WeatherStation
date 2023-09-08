from display_func import DISP_CONTROL
from time_ext import TIME_EXT
from data_conditioning import SENSOR_DATA
from micropython import const
from adafruit_io_req import AdafruitIO
from ws_wlan import WS_WLAN
from time import sleep

import my_secrets

lines = ['', '', '', '']
#d = DISP_CONTROL(lines)
#td = TIME_EXT()
#sd = SENSOR_DATA()
af = AdafruitIO(aio_username=my_secrets.ADAFRUIT_ID, aio_key=my_secrets.ADAFRUIT_KEY)
wl = WS_WLAN(debugRequired=True)

firstData = False

_VERSION        	= const(100)

_SM_INIT			= const(0)
_SM_DO_CONNECT		= const(1)
_SM_IDLE			= const(2)
_SM_UPDATE_RTC		= const(3)
_SM_UPDATE_VALUES	= const(5)
_SM_DO_RECONNECT	= const(10)

smStateVariable = _SM_INIT

wl.set_SSID(my_secrets.WIFI_ID)
wl.set_WPA2_Password(my_secrets.WIFI_PASS)

while True:
    wl.runStateMachine()
    sleep(0.2)

'''
    if smStateVariable == _SM_INIT :
        
        smStateVariable = _SM_DO_CONNECT
        
    elif smStateVariable == _SM_DO_CONNECT :

        smStateVariable = _SM_IDLE

    elif smStateVariable == _SM_IDLE :

        sd.updateValues()
        td.updateUptime()
        
        insTemp = sd.getTemp_DegC()
        insPres = sd.getPressure_hPa()
        insHumd = sd.getHumidity_pc()

        if td.isNewSecond() == True:
            firstData = True
            sd.updateSecondValuesAll()
            avgTemp = sd.getAverageTempStr(60)
            avgPres = sd.getAveragePressureStr(60)
            avgHumd = sd.getAverageHumidityStr(60)
            if (td.get_totalUptimeSecs() % 60) == 0:
                print(f"Uptime {td.get_totalUptimeSecs()}")
                print(avgTemp)
                af.sendDatapoint('bme280-tempdegc', insTemp)

        if firstData:
            d.setLine(line=0, newString=td.getTimeDateString())
            d.setLine(line=1, newString=f"{insTemp:.2f} {avgTemp} C")
            d.setLine(line=2, newString=f"{insPres:.2f} {avgPres}")
            d.setLine(line=3, newString=f"{insHumd:.2f} {avgHumd} %")
            d.showLines()

        smStateVariable = _SM_IDLE

    elif smStateVariable == _SM_UPDATE_RTC :

        smStateVariable = _SM_IDLE

    elif smStateVariable == _SM_UPDATE_VALUES :

        smStateVariable = _SM_IDLE

    elif smStateVariable == _SM_DO_RECONNECT :
    
        smStateVariable = _SM_IDLE

    else:
        
        smStateVariable = _SM_INIT
'''
