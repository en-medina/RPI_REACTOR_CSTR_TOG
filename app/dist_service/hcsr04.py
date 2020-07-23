import time
import logging
try:
	import RPi.GPIO as GPIO
except Exception:
  logging.critical("RPi.GPIO package not found... creating None variable for testing purpose only...")
  GPIO = None

class HCSR04():

	def __init__(self, GPIO_ECHO, GPIO_TRIGGER):
		#GPIO Mode (BOARD / BCM) this setmode is apply in global config
		#GPIO.setmode(GPIO.BCM)

		#set GPIO Pins
		self.GPIO_TRIGGER = GPIO_TRIGGER
		self.GPIO_ECHO = GPIO_ECHO
		self.timeout = time.time()
		#set GPIO direction (IN / OUT)
		GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
		GPIO.setup(GPIO_ECHO, GPIO.IN)

	def is_timed_out(self, value):
		return value > self.timeout

	def distance(self):
		# set Trigger to HIGH

		StartTime = time.time()
		StopTime = time.time()

		while True:
			self.timeout = time.time() + 2
			GPIO.output(self.GPIO_TRIGGER, True)

			# set Trigger after 0.01ms to LOW
			time.sleep(0.00001)
			GPIO.output(self.GPIO_TRIGGER, False)

			StartTime = time.time()
			StopTime = time.time()

			# save StartTime
			while GPIO.input(self.GPIO_ECHO) == 0:
					StartTime = time.time()
					if self.is_timed_out(StartTime):
						break

			# save time of arrival
			while GPIO.input(self.GPIO_ECHO) == 1:
					StopTime = time.time()
					if self.is_timed_out(StopTime):
						break

			if not self.is_timed_out(StartTime):
				break
			time.sleep(0.001)
		# time difference between start and arrival
		TimeElapsed = StopTime - StartTime
		# multiply with the sonic speed (34300 cm/s)
		# and divide by 2, because there and back
		distance = (TimeElapsed * 34300) / 2
		return round(distance, 2)