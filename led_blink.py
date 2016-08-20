import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)

def pinMap(x):
	return {
		0: 7,
		1: 33,
		2: 35,
		3: 37
	}[x]

try:
	for i in range(50):
		x = i % 4;
		GPIO.output(pinMap(x), True)
		time.sleep(1)
		GPIO.output(pinMap(x), False)
		time.sleep(1)
	
	GPIO.cleanup()

except KeyboardInterrupt:
	GPIO.cleanup()
