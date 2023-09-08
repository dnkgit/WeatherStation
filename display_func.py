from machine import Pin, I2C
import time
import sh1106

NUM_LINES = 4
CHAR_HEIGHT = 12

LINE1 = 0 * CHAR_HEIGHT
LINE2 = 1 * CHAR_HEIGHT
LINE3 = 2 * CHAR_HEIGHT
LINE4 = 3 * CHAR_HEIGHT

VERSION = 1.00

class DISP_CONTROL:

    def __init__(self, initStrings):
        
        self.i2c=I2C(0,sda=Pin(20), scl=Pin(21), freq=400000)    #initializing the I2C method 
        self.display = sh1106.SH1106_I2C(128,64,self.i2c)

        self.workingSetLines = list(initStrings)	# working set
        self.initSetLines = list(initStrings)		# Golden set 

        self.showInitText()
    
    def showInitText(self):
        scrollText = '                (C) D Lloyd 2023....'
        while scrollText[0] != 'C': 
            self.display.fill(0)
            self.display.text("display_func", 0, LINE1, 1)
            self.display.text(f"V{VERSION}", 0, LINE2, 1)
            self.display.text("----------------", 0, LINE3, 1)
            self.display.text(scrollText, 0, LINE4, 1)
            self.display.show()
            scrollText = scrollText[1:]
            time.sleep(0.01)
        time.sleep(0.5)
        self.display.fill(0)
        self.display.show()

    def showLines(self):
        line = 0
        y_pos = 0
        self.display.fill(0)
        while line < NUM_LINES:
            self.display.text(self.workingSetLines[line], 0, y_pos, 1)
            line += 1
            y_pos += CHAR_HEIGHT
        self.display.show()

    def setLines(self, allLines):
        if len(allLines) == 4:
            self.workingSetLines = list(allLines)

    def getLines(self):
        return self.workingSetLines

    def getLine(self, line):
        return self.workingSetLines[line]

    def setLine(self, line, newString):
        self.workingSetLines[line] = newString
 
    def getNumLines(self):
        return len(self.workingSetLines)
    
    def restoreInitLines(self):
        self.workingSetLines = list(self.initSetLines)