import logging
import importlib.util
from time import sleep

try:
	import RPi.GPIO as GPIO
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	
except Exception:
    logging.critical("RPi.GPIO package not found... creating None variable for testing purpose only...")
    GPIO = None

spec = importlib.util.spec_from_file_location("AnalogIn, ADS1115", "../dist_service/hcsr04.py")
hcs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hcs)

if '__main__' == __name__:
	echoPin = int(input('Enter Echo PIN: '))
	triggerPin = int(input('Enter Echo Trigger PIN: '))
	distance = hcs.HCSR04(echoPin, triggerPin)
	try:
		while True:
			cnt = 10
			acc = 0
			for i in range(cnt):
				acc += distance.distance()
			acc = acc/cnt
			print('The distance is', acc)
			sleep(2)
	except Exception:
		print("Measurement stopped by User")
		GPIO.cleanup()
