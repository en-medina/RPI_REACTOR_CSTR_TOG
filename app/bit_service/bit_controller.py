from threading import Lock
import logging
try:
	import RPi.GPIO as GPIO
except Exception:
    logging.critical("RPi.GPIO package not found... creating None variable for testing purpose only...")
    GPIO = None

#GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

class BitController():

	def __init__(self, pinNumber, initialState = 0):
		#GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output
		self._pinNumber = pinNumber 
		self._futereState = initialState
		self._currentState = initialState
		self._delay = 0
		self._changeNotified = False
		self._lock = Lock()
		self._possibleState = (GPIO.LOW, GPIO.HIGH)
		#GPIO.output(ledPin, self._possibleState[self._futereState])

	def __str__(self):
		with self.lock:
			return str(self._pinNumber)

	@property
	def notification(self):
		with self._lock:
			return self._changeNotified

	@property
	def currentState(self):
		with self.lock:
			return self._currentState

	@property
	def delay(self):
		with self.lock:
			return self._delay
		
	def notify_change(self, futureState, delay = 0, reverse = False):
		with self._lock:
			if reverse:
				self.futureState = futureState
				self._apply_change()
				self.futureState = not futureState
			else:
				self._futereState = futureState
			self._changeNotified = True
			self._delay = delay

	def _apply_change(self):
		self._currentState = self.futureState
		#GPIO.output(ledPin, self._possibleState[self._futereState])
		self._changeNotified = False
		self._delay = 0

	def apply_change(self):
		with self._lock:
			self._apply_change()
