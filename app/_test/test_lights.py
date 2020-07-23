import RPi.GPIO as GPIO  
GPIO.cleanup() 
GPIO.mode(GPIO.BOARD)
pins = [33, 31, 29, 32, 13]
try:
	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(self.GPIO_TRIGGER, GPIO.HIGH)
	sleep(10)
	for pin in pins:
		GPIO.output(self.GPIO_TRIGGER, GPIO.LOW)
except Exception:
	GPIO.cleanup()
GPIO.cleanup()