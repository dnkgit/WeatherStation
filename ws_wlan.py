import network
import machine
from time import sleep
from micropython import const
from time_ext import TIME_EXT

WLAN_STATE_INIT                 = const(0)
WLAN_STATE_FIRST_CONNECTION     = const(1)
WLAN_STATE_FAILED_TO_CONNECT    = const(2)
WLAN_STATE_CONNECTED            = const(3)
WLAN_STATE_DISCONNECTED         = const(4)
WLAN_STATE_RECONNECTED          = const(5)

class WS_WLAN():

    def __init__(self, debugRequired=False, ssid='', wpaPassword=''):

        self.ssid = ssid
        self.wpa2_passwd = wpaPassword

        self.numberOfReconnections = 0

        self.stateMachineState = WLAN_STATE_INIT

        self.doDebug = debugRequired

        self.te = TIME_EXT()

    def runStateMachine(self):
        
        if self.stateMachineState == WLAN_STATE_INIT:
            
            self.debugPrint(showTime=True, debugString="WLAN_STATE_INIT")

            self.init_WLAN()
            self.get_accessPoints()
            self.numberOfReconnections = 0
            self.stateMachineState = WLAN_STATE_FIRST_CONNECTION
            self.doDisconnect()
            
        elif self.stateMachineState == WLAN_STATE_FIRST_CONNECTION:
    
            self.debugPrint(showTime=True, debugString="WLAN_STATE_FIRST_CONNECTION")

            self.doConnect()
            
            if (self.wlan.isconnected() == True) and (self.wlan.status() == network.STAT_GOT_IP):
                print(f"Connected to {self.ssid}...")
                self.show_WLAN_Status()
                self.show_WLAN_ifconfig()
                self.stateMachineState = WLAN_STATE_CONNECTED
                self.debugPrint(showTime=True, debugString="WLAN_STATE_CONNECTED")
            else:
                self.stateMachineState = WLAN_STATE_FAILED_TO_CONNECT                
    
        elif self.stateMachineState == WLAN_STATE_FAILED_TO_CONNECT:
            
            self.debugPrint(showTime=True, debugString="WLAN_STATE_FAILED_TO_CONNECT")

            stateMachineState = WLAN_STATE_DISCONNECTED                
            
        elif self.stateMachineState == WLAN_STATE_CONNECTED:
            
            if (self.wlan.isconnected() == False) or (self.wlan.status() != network.STAT_GOT_IP):
                self.stateMachineState = WLAN_STATE_DISCONNECTED                
            
        elif self.stateMachineState == WLAN_STATE_DISCONNECTED:

            self.debugPrint(showTime=True, debugString="WLAN_STATE_DISCONNECTED")

            self.doDisconnect()
            self.numberOfReconnections += 1
            self.stateMachineState = WLAN_STATE_RECONNECT

        elif self.stateMachineState == WLAN_STATE_RECONNECT:

            self.debugPrint(showTime=True, debugString="WLAN_STATE_RECONNECT")

            self.doConnect()
            
            if (self.wlan.isconnected() == True) and (self.wlan.status() == network.STAT_GOT_IP):
                print(f"Reconnected to {self.ssid}...")
                self.show_WLAN_Status()
                self.show_WLAN_ifconfig()
                self.stateMachineState = WLAN_STATE_CONNECTED
                self.debugPrint(showTime=True, debugString="WLAN_STATE_CONNECTED")
            else:
                self.stateMachineState = WLAN_STATE_FAILED_TO_CONNECT                

        else:
            self.stateMachineState = WLAN_STATE_INIT

    def init_WLAN(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.config(pm = 0xa11140)	# Set high power
        
    def get_accessPoints(self):        
        accessPoints = self.wlan.scan()	# Find SSIDs
        self.show_accessPoints(accessPoints)

    def show_accessPoints(self, accessPoints):
        
        for ap in accessPoints:
            (ssid, bssid, channel, RSSI, security, hidden) = ap
            print(f"[{ssid}] [{bssid}] [{channel}] [{RSSI}] [{security}] [{hidden}]")
            print( "------------------------------")
            '''
            print(f"ssid     : {ssid}")
            print(f"bssid    : {bssid}")
            print(f"channel  : {channel}")
            print(f"RSSI     : {RSSI}")
            print(f"security : {security}")
            print(f"hidden   : {hidden}")
            '''
            print( "------------------------------")

    def set_SSID(self, newSSID):
        self.ssid = newSSID

    def set_WPA2_Password(self, newPassword):
        self.wpa2_passwd = newPassword

    def show_WLAN_Status(self, comment='n/a'):
        
        status = self.wlan.status()
        status_str = self.convert_WLAN_status_to_string(status)                
        isConnected = self.wlan.isconnected()
        print(f"WLAN Status   : [{status}][{status_str}][{isConnected}][{comment}]")

    def show_WLAN_ifconfig(self):
        data = self.wlan.ifconfig()
        print(f"WLAN ifconfig : {data}")

    def doConnect(self):

        if (self.ssid != '') and (self.wpa2_passwd != ''):

            #self.show_WLAN_Status()
            #self.show_WLAN_ifconfig()

            if self.wlan.isconnected() == True:
                self.doDisconnect()
                #self.show_WLAN_ifconfig()

            print(f"doConnect : Attempting to connect to {self.ssid}...")
            self.wlan.connect(ssid=self.ssid, key=self.wpa2_passwd)

            while not self.wlan.isconnected() and self.wlan.status() >= 0:
                #self.show_WLAN_Status()
                #self.show_WLAN_ifconfig()
                sleep(0.5)

            print("doConnect : Connected, info:")
            self.show_WLAN_Status()
            self.show_WLAN_ifconfig()

        else:
            print('WSLAN ERROR: No password or SSID to select')

    def doDisconnect(self):
        self.wlan.disconnect()

    def isConnectionActive(self):
        return self.wlan.isconnected()

    def get_WifiNetworksScanned(self):
        networks = self.wlan.scan()
        return networks

    def debugPrint(self, debugString='', showTime=False):
        
        if self.doDebug:
            print("")
            if showTime:
                self.te.updateTime()
                timeString = self.te.getCurrentTimeAsString()
                print(f"{timeString} : {debugString}")
            else:
                print(f"{debugString}")
    
    def convert_WLAN_status_to_string(self, statusValue):
        retVal = 'UNKNOWN'

        '''
        print(network.STAT_IDLE)
        print(network.STAT_CONNECTING)
        print(network.STAT_WRONG_PASSWORD)
        print(network.STAT_NO_AP_FOUND)
        print(network.STAT_CONNECT_FAIL)
        print(network.STAT_GOT_IP)
        print("-----")
        '''

        if statusValue == 0:
            retVal = 'STAT_IDLE'
        elif statusValue == 1:
            retVal = 'STAT_CONNECTING'
        elif statusValue == -3:
            retVal = 'STAT_WRONG_PASSWORD'
        elif statusValue == -2:
            retVal = 'STAT_NO_AP_FOUND'
        elif statusValue == -1:
            retVal = 'STAT_CONNECT_FAIL'
        elif statusValue == 3:
            retVal = 'STAT_GOT_IP'

        return retVal
