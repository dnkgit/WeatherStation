import bme280
from machine import Pin, I2C

class SENSOR_DATA:
    
    def __init__(self, samplePeriods=0):
        self.i2c=I2C(0,sda=Pin(20), scl=Pin(21), freq=400000)
        self.updateValues()

    def updateValues(self):
        self.bme280 = bme280.BME280(i2c=self.i2c, useDebug=False)
        
    def getTemp_DegC(self):
        return float(self.bme280.values[0])
    
    def getPressure_hPa(self):
        return float(self.bme280.values[1])

    def getHumidity_pc(self):
        return float(self.bme280.values[2])
