import bme280
from machine import Pin, I2C

class SENSOR_DATA:
    
    def __init__(self):
        self.i2c=I2C(0,sda=Pin(20), scl=Pin(21), freq=400000)
        self.bme280 = bme280.BME280(i2c=self.i2c, useDebug=False)

        self.lastMinTemp = []
        self.lastMinPressure = []
        self.lastMinHumidity = []

        print("To complete. Hour and Day averages")
        print("Hour average is last 60 values from minute rollovers")
        print("Day average is last 24 values from hour rollovers")
        
        self.lastHourTemp = []
        self.lastHourPressure = []
        self.lastHourHumidity = []
        
        self.lastDayTemp = []
        self.lastDayPressure = []
        self.lastDayHumidity = []

    def getAverageTempStr(self, last_n):
        #print(self.lastMinTemp[:10])
        return self.calculateAverage(self.lastMinTemp, last_n)

    def getAveragePressureStr(self, last_n):
        #print(self.lastMinPressure[:10])
        return self.calculateAverage(self.lastMinPressure, last_n)

    def getAverageHumidityStr(self, last_n):
        #print(self.lastMinHumidity[:10])
        return self.calculateAverage(self.lastMinHumidity, last_n)

    def calculateAverage(self, data, last_n):
        subset = data[:last_n]
        sum_subset = sum(subset)
        avg = sum_subset / len(subset)
        #print(f"subset {subset}")
        #print(f"sum {sum_subset}")
        #print(f"avg {avg}")
        result = f"{avg:.02f}"
        return result

    def updateSecondValuesAll(self):
        self.bme280 = bme280.BME280(i2c=self.i2c, useDebug=False)
        self.updateSecondValuesTemperature()
        self.updateSecondValuesPressure()
        self.updateSecondValuesHumidity()

    def updateSecondValuesTemperature(self):
        if len(self.lastMinTemp) < 60:
            pass
        else:
            self.lastMinTemp.pop()
        self.lastMinTemp.insert(0, self.getTemp_DegC())

    def updateSecondValuesPressure(self):
        if len(self.lastMinPressure) < 60:
            pass
        else:
            self.lastMinPressure.pop()
        self.lastMinPressure.insert(0, self.getPressure_hPa())

    def updateSecondValuesHumidity(self):
        if len(self.lastMinHumidity) < 60:
            pass
        else:
            self.lastMinHumidity.pop()
        self.lastMinHumidity.insert(0, self.getHumidity_pc())

    def updateValues(self):
        self.bme280 = bme280.BME280(i2c=self.i2c, useDebug=False)
        
    def getTemp_DegC(self):
        return float(self.bme280.values[0])
    
    def getPressure_hPa(self):
        return float(self.bme280.values[1])

    def getHumidity_pc(self):
        return float(self.bme280.values[2])
