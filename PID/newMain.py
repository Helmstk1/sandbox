import board
import time
import simpleio
import analogio

from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

from lcd.lcd import CursorMode

# Talk to the LCD at I2C address 0x27.
# The number of rows and columns defaults to 4x20, so those
# arguments could be omitted in this case.
lcd1 = LCD(I2CPCF8574Interface(board.I2C(), 0x3f), num_rows=2, num_cols=16)
lcd2 = LCD(I2CPCF8574Interface(board.I2C(), 0x27), num_rows=2, num_cols=16)

posPot = analogio.AnalogIn(board.A1)
valPot = analogio.AnalogIn(board.A2)

PID = False
values = [3.56, 3.56, 1.23, PID]
oldValues = [0, 0, 0, 0]

kP = 0
kI = 1
kD = 2
pid = 3

def setScreen():
    '''Prints out all static messages at once'''
    # Start at the first line, first column (numbering from zero).
    lcd1.set_cursor_pos(0, 0)
    lcd1.print("kP=")
    lcd1.print(str(values[kP]))

    lcd1.set_cursor_pos(0, 7)
    lcd1.print(" kD=")
    lcd1.print(str(values[kD]))
    lcd1.set_cursor_pos(0, 2)

    lcd1.set_cursor_pos(1, 0)
    lcd1.print("kI=")
    lcd1.print(str(values[kI]))

    lcd1.set_cursor_pos(1, 8)
    lcd1.print("PID=")
    
    if values[pid]:
        lcd1.set_cursor_pos(1, 12)
        lcd1.print("On  ")
    else:
        lcd1.set_cursor_pos(1, 12)
        lcd1.print("Off ")
        
    lcd2.set_cursor_pos(0, 0)
    lcd2.print("Setpoint: ")
    lcd2.set_cursor_pos(1, 0)
    lcd2.print("ActualRPM: ")

def moveCursor():
    time.sleep(.1)
    cursorPos = simpleio.map_range(posPot.value, 0, 65535, 0, 5)
    
    print(cursorPos)
    if cursorPos < 4:
        if cursorPos < 1:
            lcd1.set_cursor_pos(0, 2)
            # print("0,2")
        elif cursorPos < 2:
            lcd1.set_cursor_pos(1, 2)
        elif cursorPos < 3:
            lcd1.set_cursor_pos(0, 10)
        elif cursorPos < 4:
            lcd1.set_cursor_pos(1, 11)
        
        lcd1.set_cursor_mode(CursorMode.BLINK)
        lcd2.set_cursor_mode(CursorMode.HIDE)
            
    else:
        lcd1.set_cursor_mode(CursorMode.HIDE)
        lcd2.set_cursor_mode(CursorMode.BLINK)
        if cursorPos == 4:
            lcd2.set_cursor_pos(0, 10)
        else:
            lcd2.set_cursor_pos(1, 11)
        
    return cursorPos

    
setScreen()
# print(values[kP], "\t", values[kI], "\t", values[kD], "\t", values[3])

time.sleep(5)


while True:
    valSelect = int(moveCursor())
    print(valSelect)
    if valSelect == 0:
        values[kP] = simpleio.map_range(valPot.value, 0, 65535, 0.0, 10.0)
    if valSelect == 1:
        values[kI] = simpleio.map_range(valPot.value, 0, 65535, 0.0, 10.0)
    if valSelect == 2:
        values[kD] = simpleio.map_range(valPot.value, 0, 65535, 0.0, 10.0)
    if valSelect == 3:
        if valPot.value > (65535/2):
            PID = True
            lcd1.set_cursor_pos(1, 12)
            lcd1.print("On  ")
        else:
            PID = False
            lcd1.set_cursor_pos(1, 12)
            lcd1.print("Off ")
    if values != oldValues:
        setScreen()
    
    print(values, "\t", oldValues)
    
    oldValues = values
    time.sleep(1)

    
    
    
 
