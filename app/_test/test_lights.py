import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BOARD) # BOARD pin-numbering scheme
GPIO.setwarnings(False)
pins = [33, 31, 29, 32, 13]
try:
	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(self.GPIO_TRIGGER, GPIO.HIGH)
	sleep(10)
	for pin in pins:
		GPIO.output(self.GPIO_TRIGGER, GPIO.LOW)
except Exception as e:
	print(e)
	GPIO.cleanup()
GPIO.cleanup()
