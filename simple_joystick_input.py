import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(33, GPIO.IN)
GPIO.setup(35, GPIO.IN)
GPIO.setup(37, GPIO.IN)
try:
	while True:
		if GPIO.input(35) > 0:
			GPIO.output(7, True)
			#print(GPIO.input(35))
		else:
			GPIO.output(7, False)

	#GPIO.cleanup()

except KeyboardInterrupt:
	GPIO.cleanup()
