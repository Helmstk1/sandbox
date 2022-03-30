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
valPot = analogio.AnalogIn(board.A3)

kP = 3.56
kI = 3.56
kD = 1.23
PID = False

def setScreen():
    '''Prints out all static messages at once'''
    # Start at the first line, first column (numbering from zero).
    lcd1.clear()
    lcd2.clear()

    lcd1.set_cursor_pos(0, 0)
    lcd1.print("kP=")
    lcd1.print(str(kP))

    lcd1.set_cursor_pos(0, 7)
    lcd1.print(" kD=")
    lcd1.print(str(kD))
    lcd1.set_cursor_pos(0, 2)

    lcd1.set_cursor_pos(1, 0)
    lcd1.print("kI=")
    lcd1.print(str(kI))

    lcd1.set_cursor_pos(1, 8)
    lcd1.print("PID=")

    lcd2.set_cursor_pos(0, 0)
    lcd2.print("Setpoint: ")
    lcd2.set_cursor_pos(1, 0)
    lcd2.print("ActualRPM: ")

def moveCursor():
    #print("setting cursor position")
    # cursorPos = simpleio.map_range(posPot.value, 0, 65535, 0, 5)
    cursorPos = 4
    

    if cursorPos < 4:
        lcd1.set_cursor_mode(CursorMode.BLINK)
        lcd2.set_cursor_mode(CursorMode.HIDE)
        if cursorPos is 0:
            lcd1.set_cursor_pos(0, 2)
        elif cursorPos is 1:
            lcd1.set_cursor_pos(1, 2)
        elif cursorPos is 2:
            lcd1.set_cursor_pos(0, 10)
        elif cursorPos is 3:
            lcd1.set_cursor_pos(1, 11)
            
    else:
        lcd1.set_cursor_mode(CursorMode.HIDE)
        lcd2.set_cursor_mode(CursorMode.BLINK)
        if cursorPos is 4:
            lcd2.set_cursor_pos(0, 10)
        else:
            lcd2.set_cursor_pos(1, 11)
        
    return cursorPos

    

        





setScreen()

# time.sleep(1)


while True:
    moveCursor()
    '''
    if PID:
       lcd1.set_cursor_pos(1, 12)
       lcd1.print("On  ")
    else:
       lcd1.set_cursor_pos(1, 12)
       lcd1.print("Off ")
    '''
 
