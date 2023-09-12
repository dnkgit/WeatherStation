import machine
import ntptime

class REALTIMECLOCK:
    
    def __init__(self):
        self.rtc = machine.RTC()
          
    def syncNtpTime(self):
        ntptime.settime()
  
    def getRtcTime(self):
        return(str(self.rtc.datetime()))
