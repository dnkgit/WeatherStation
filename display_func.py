from machine import Pin, I2C
import time
import sh1106

_NUM_LINES = 5
_CHAR_HEIGHT = 12
_MAX_LINE_LEN = 16

_LINE1 = 0 * _CHAR_HEIGHT
_LINE2 = 1 * _CHAR_HEIGHT
_LINE3 = 2 * _CHAR_HEIGHT
_LINE4 = 3 * _CHAR_HEIGHT
_LINE5 = 4 * _CHAR_HEIGHT

VERSION = 1.00

class DISP_CONTROL:

    def __init__(self):
        
        self.i2c=I2C(0,sda=Pin(20), scl=Pin(21), freq=400000)    #initializing the I2C method 
        self.display = sh1106.SH1106_I2C(128,64,self.i2c)

        self.frameBuf = [['', '', '', '', ''],['', '', '', '', '']]
        self.frameBufIdx = 0

        self.showInitText()
    
    def showInitText(self):
        self.display.fill(0)
        self.display.text("display_func"    , 0, _LINE1, 1)
        self.display.text(f"V{VERSION}"     , 0, _LINE2, 1)
        self.display.text("----------------", 0, _LINE3, 1)
        self.display.text("(C) D Lloyd 2023", 0, _LINE4, 1)
        self.display.text("----------------", 0, _LINE5, 1)
        self.display.show()
        time.sleep(1.0)

    def toggleFrameBuffer(self):
        if self.frameBufIdx == 0:
            self.frameBufIdx = 1
        else:
            self.frameBufIdx = 0
    
    def runDisplay(self):
        self.showDispSet(self.frameBufIdx)

    def showDispSet(self, frameBuxIdx):
        line = 0
        y_pos = 0
        self.display.fill(0)
        while line < _NUM_LINES:
            self.display.text(self.frameBuf[frameBuxIdx][line], 0, y_pos, 1)
            line += 1
            y_pos += _CHAR_HEIGHT
        self.display.show()

    def setDispSetLine(self, set_idx, line_idx, text):
            if set_idx < len(self.frameBuf):
                if line_idx < len(self.frameBuf[set_idx]):
                    self.frameBuf[set_idx][line_idx] = text[:_MAX_LINE_LEN]
                    
    def getLines(self, frameBufIdx):
        return self.frameBuf[frameBufIdx]

    def getLine(self, frameBufIdx, line):
        return self.frameBuf[frameBufIdx][line]
