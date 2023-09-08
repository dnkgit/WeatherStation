# if python
# import requests
# if micropython
import urequests as requests
from time import sleep

class AdafruitIO():

    def __init__(self, aio_username='', aio_key=''):
        
        self.aio_username = aio_username
        self.aio_key = aio_key     
        self.waitTimeSec = 0.5

    def setUsername(self, newUsername):
        
        self.aio_username = newUsername

    def setUserKey(self, newUserKey):
        
        self.aio_key = newUserKey

    def setPostSendWaitTime(self, newWaitTimeSec):
        
        self.waitTimeSec = newWaitTimeSec

    def sendDatapoint(self, feedKey, dataValue):
        
        self.doDataSend(feedKey, dataValue)

    def sendDataPoints(self, dataPoints):

        for itemDict in dataPoints:
            self.doDataSend(itemDict['name'], itemDict['value'])

    def doDataSend(self, feedKey, feedValue):
            
            url = 'https://io.adafruit.com/api/v2/' + self.aio_username  + '/feeds/' + feedKey +'/data'
            body = {'value': str(feedValue)}
            headers = {'X-AIO-Key': self.aio_key, 'Content-Type': 'application/json'}
            
            try:
                r = requests.post(url, json=body, headers=headers)
                # print(r.text)
                r.close()
            except Exception as e:
                print(f"Adafruit Send Exception [{e}]")

            sleep(self.waitTimeSec)
