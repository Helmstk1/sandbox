# PID w/ rotary encoder, based off Arduino example from Dr. Shields

''' OK, so the encoder would be cool, but it makes so much extra work!!'''

import board
import time
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
import rotaryio
# EEPROM?  timerone.h?  Clickencoder.h?

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

''' Some Timer1 stuff that may be related to pwm or rotary encoder
	Timer1.initialize(1000);
  	Timer1.attachInterrupt(timerIsr); 
  	last = -1;
'''

'''LCD is already setup, no init needed
	lcd.begin();
	lcd.backlight();
	lcd.createChar(0, fullArrow);
	lcd.createChar(1, emptyArrow);
	lcd.createChar(2, smallArrow);
	lcd.home();
	lcd.print(" PID:OFF ");
	lcd.print("S:    0");
	lcd.setCursor(0,1);
	lcd.print(" kP .");
	lcd.print(fixSpeed(PID[0],2,"0"));
	lcd.print(" A:    0");
'''

''' void moveCursor() {
	for(int i=0; i<4; i++) {
		lcd.setCursor(cols[i],rows[i]);
		if(i==cursorPos) 
			lcd.write(arrowSize);
		else
			lcd.print(" ");
	}
}
'''
while True: 
	now = time.monotonic()
	if now > (lastRPM + msDelay):
		calcRPM()
		setMotor()
		lastRPM = time.monotonic()
	
	value = value + encoderValue #rewrite with correct encoder code?

	if value is not last:
		if value > last:
			encoderBump = 1
		else:
			encoderBump = -1
		if arrowSize is 2: 		# you're moving the cursor
			cursorPos += encoderBump
			if cursorPos > 3
				cursorPos = 0
			if cursorPos < 0
				cursorPos = 4
		else:   				# You're changing a value
			if cursorPos is 0:
				lcd.setCursor(6,0)
				pidToggle = !pidToggle
				if pidToggle is True:
					lcd.print("N ")
				else:
					lcd.print("FF")
			elif cursorPos is 1: # You're cycling through Kp,Ki,Kd
				lcd.setCursor(2,0)
				pidIndex += encoderBump
				if pidIndex > 2:
					pidIndex = 0
				if pidIndex < 0:
					pidIndex = 2
				lcd.print(pidText[pidIndex])
				lcd.print(" .")
				lcd.print(fixSpeed(PID[pidIndex],2,"0"))
			elif cursorPos is 3: # ?
				lcd.setCursor(11, 0)
				if (setPoint < maxSpeed):
					setPoint += encoderBump
				setPointAct = map(setpoint,0,255,0,maxSpeed)
				lcd.print(fixSpeed(setPointAct,4," "))
		rotCount++
	Clickencoder::button b = encoder->getButton()
	if (b is not ClickEncoder::Open):
		if b = (ClickEncoder::Clicked:):
			if(arrowSize == 0):
					arrowSize = 2
				else:
					arrowSize = 0
		if b is (ClickEncoder::Held:):
			print("Saving")
			for i in range(3):
				EEPROM.write(i,PID[i])
			saved = True
			# He cycled the lcd backlight, is that a thing? Dhalbert
		if b is (ClickEncoder::Released:):
			saved = false
	moveCursor()
	last = value

def fixSpeed(speed, max, what):
	str = ""
	for i in range(log10(speed),max):
		str += what
	str += String(speed)
	return str

def calcRPM():
	# detach the interupt:
	# detachInterrupt(digitalPinToInterrupt(interruptPin));
	RPM = count*multiplier
	lcd.setCursor(11,1)
	lcd.print(fixSpeed(RPM,4," "))
	lcd.print("    ")
	count = 0
	# Reattach the interupt function
	# attachInterrupt(digitalPinToInterrupt(interruptPin), blink, RISING);

def setMotor():
	if pidToggle:
		error = setPointAct - RPM
		P = error * PID[0]/1000
		I = I + error * PID[1]/1000
		D = (error-lastError)/(msDelay/1000) * PID[2]/1000
		drive = P + I + D






				


