import RPi.GPIO as GPIO  
from time import sleep
GPIO.setmode(GPIO.BOARD) # BOARD pin-numbering scheme
GPIO.setwarnings(False)
delay = int(input('Hola muchachos, entren el tiempo de oscilación en milisegundos [ms]'))
delay = delay / 1000.0
pin = 13
GPIO.setup(pin, GPIO.OUT)
try:
	while True:
		GPIO.output(pin, GPIO.HIGH)
		sleep(delay)
		GPIO.output(pin, GPIO.LOW)
		sleep(delay)
except Exception as e:
	print(e)
	GPIO.cleanup()
GPIO.cleanup()
