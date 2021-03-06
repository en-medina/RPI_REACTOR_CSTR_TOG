import RPi.GPIO as GPIO  
from time import sleep
GPIO.setmode(GPIO.BOARD) # BOARD pin-numbering scheme
GPIO.setwarnings(False)
pins = [33, 31, 29, 32, 13]
try:
	for pin in pins:
		GPIO.setup(pin, GPIO.OUT)
	for _ in range(2):
		for pin in pins:
			GPIO.output(pin, GPIO.HIGH)
		sleep(3)
		for pin in pins:
			GPIO.output(pin, GPIO.LOW)
except Exception as e:
	print(e)
	GPIO.cleanup()
GPIO.cleanup()
