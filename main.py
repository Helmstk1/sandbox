# Write your code here :-)
import board
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
import rotaryio


motorPin = 3
interruptPin = 2
RotaryButton = board.D12

'''
uint8_t emptyArrow = [0x10, 0x8, 0x4, 0x2, 0x4, 0x8, 0x10]
uint8_t fullArrow = [0x10, 0x18, 0x1c, 0x1e, 0x1c, 0x18, 0x10]
uint8_t smallArrow = [0x0, 0x10, 0x18, 0x1c, 0x18, 0x10]

emptyArrow = [0x10, 0x8, 0x4, 0x2, 0x4, 0x8, 0x10]
fullArrow = [0x10, 0x18, 0x1c, 0x1e, 0x1c, 0x18, 0x10]
smallArrow = [0x0, 0x10, 0x18, 0x1c, 0x18, 0x10]
'''


cols = [0, 0, 3, 8]
rows = [0, 1, 1, 0]
PID = [EEPROM.read(0),EEPROM.read(1),EEPROM.read(2)]
pidText = ["P","I","D"]

pidIndex = 0
cursorPos = 0
arrowSize = 2
# int buttonState, lastState, aState, aLastState;
selected = 0
# int kP, kI, kD;
setPoint = 0
# float setPointAct;
maxPID = 999
maxSpeed = 13000
rotCount = 0
# int encoderBump;
pidToggle = false
saved = false
lastRPM = 0.0
# long now;
msDelay = 250
float RPM;
slots = 5
# volatile int count = 0;
multiplier = 60*(1000/msDelay)/slots
# float error, lastError;
# float P, I, D, drive;

i2c = board.I2C()
# some LCDs are 0x3f... some are 0x27.
lcd = LCD(I2CPCF8574Interface(i2c, 0x3f), num_rows=2, num_cols=16)

encoder = rotaryio.IncrementalEncoder(board.D10, board.D9)
button = digitalio.DigitalInOut(RotaryButton)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP