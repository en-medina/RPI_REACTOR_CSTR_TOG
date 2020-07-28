from threading import Lock
import logging
try:
	import RPi.GPIO as GPIO
	#GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
except Exception:
    logging.critical("RPi.GPIO package not found... creating None variable for testing purpose only...")
    GPIO = None


class BitController():

	def __init__(self, pinNumber, initialState = 0):
		self._pinNumber = pinNumber 
		self._futereState = initialState
		self._currentState = initialState
		self._delay = 0
		self._changeNotified = False
		self._lock = Lock()
		self._possibleState = (GPIO.LOW, GPIO.HIGH)
		GPIO.setup(self._pinNumber, GPIO.OUT) # pinNumber set as output
		GPIO.output(pinNumber, self._possibleState[self._futereState])

	def __str__(self):
		with self._lock:
			return str(self._pinNumber)

	@property
	def notification(self):
		with self._lock:
			return self._changeNotified

	@property
	def currentState(self):
		with self._lock:
			return self._currentState

	@property
	def delay(self):
		with self._lock:
			return self._delay
		
	def notify_change(self, futureState, delay = 0, reverse = False):
		with self._lock:
			if reverse:
				self._futereState  = futureState
				self._apply_change()
				self._futereState  = not futureState
			else:
				self._futereState = futureState
			self._changeNotified = True
			self._delay = delay

	def _apply_change(self):
		self._currentState = self._futereState
		GPIO.output(self._pinNumber, self._possibleState[self._futereState])
		self._changeNotified = False
		self._delay = 0

	def apply_change(self):
		with self._lock:
			self._apply_change()

	def quick_change(self, state):
		with self._lock:
			GPIO.output(self._pinNumber, self._possibleState[state])

	def quick_notify(self, state):
		with self._lock:
			self._changeNotified = state
