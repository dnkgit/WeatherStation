from machine import RTC

YEAR = 0
MONTH = 1
DAY = 2
HOUR = 4
MINUTE = 5
SECOND = 6

class TIME_EXT:
    
    def __init__(self):
        self.rtc = RTC()
        self.currentTime = self.rtc.datetime()
        self.lastSecond = self.currentTime[SECOND]
        self.lastMinute = self.currentTime[MINUTE]
        self.lastHour = self.currentTime[HOUR]
        
        self.totalUptime = {}
        self.totalUptime['LastSec'] = self.currentTime[SECOND]
        self.totalUptime['Seconds'] = 0

    def updateUptime(self):
        self.updateTime()
        if self.totalUptime['LastSec'] != self.currentTime[SECOND]:
            self.totalUptime['Seconds'] += 1
            self.totalUptime['LastSec'] = self.currentTime[SECOND]

    def get_totalUptimeSecs(self):
        return self.totalUptime['Seconds']

    def isNewSecond(self):
        returnValue = False
        self.updateTime()
        if self.lastSecond != self.currentTime[SECOND]:
            returnValue = True
        self.lastSecond = self.currentTime[SECOND]
        return returnValue

    def isNewMinute(self):
        returnValue = False
        self.updateTime()
        if self.lastMinute != self.currentTime[MINUTE]:
            returnValue = True
        self.lastMinute = self.currentTime[MINUTE]
        return returnValue

    def isNewHour(self):
        returnValue = False
        self.updateTime()
        if self.lastHour != self.currentTime[HOUR]:
            returnValue = True
        self.lastHour = self.currentTime[HOUR]
        return returnValue

    def updateTime(self):
        self.currentTime = self.rtc.datetime()

    def getCurrentDateAsString(self):
        currentDate = '%02d/%02d/%04d' % (self.currentTime[DAY], self.currentTime[MONTH], self.currentTime[YEAR])
        return currentDate

    def getCurrentTimeAsString(self):
        currentTime = '%02d:%02d:%02d' % (self.currentTime[HOUR], self.currentTime[MINUTE], self.currentTime[SECOND])
        return currentTime

    def getTimeDateString(self):
        timeString = '%02d:%02d:%02d %02d/%02d' % (self.currentTime[HOUR], self.currentTime[MINUTE], self.currentTime[SECOND], self.currentTime[DAY], self.currentTime[MONTH])
        return timeString

    def getSeconds(self):
        return self.currentTime[SECOND]

    def getMinutes(self):
        return self.currentTime[MINUTE]

    def getHours(self):
        return self.currentTime[HOUR]

    def getDayOfMon(self):
        return self.currentTime[DAY]

    def setTime(self, newTime):
        pass