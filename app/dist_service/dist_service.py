#from .hcsr04 import HCSR04
import concurrent.futures
import shared_module.helpers as helpers
from time import sleep
import logging 
import random

import random 
_intervalMeasureTime = float()
_startLoop = bool()
_isDebug = bool()
_debugIterAmount = int()
_serviceName = str()

def init_dist(pipeline):
	'''
	function for initialize and run DIST module and sensors
	:param queue pipeline: queue class for pushing data
	'''
	logging.info('Starting DIST Service...')

	global _isDebug, _startLoop, _intervalMeasureTime, _debugIterAmount, _serviceName

	config = helpers.json2dict('config.json', __file__)
	_intervalMeasureTime = config['dist']['intervaltime']
	_startLoop = config['dist']['loop']
	_isDebug = config['dist']['debug']
	_debugIterAmount = config['dist']['iter']
	_serviceName = config['dist']['threadname']

	dist_params = config['dist']['pinout']

	if _isDebug:
		logging.warning(f'({_serviceName}) - internal debug is enable...')

	with concurrent.futures.ThreadPoolExecutor(max_workers=3, thread_name_prefix = _serviceName) as executor:

		futureException = {
			executor.submit(
				hcsr04_pool, 
				key,
				dist_params[key]['echo'], 
				dist_params[key]['trigger'], 
				pipeline
				): key for key in dist_params.keys()
		}

		for futureErrors in concurrent.futures.as_completed(futureException):
			threadName = futureException[futureErrors]
			try:
				data = futureErrors.result()
			except Exception as exc:
				logging.error(f'({_serviceName}) - \'{threadName}\' generated an exception: {exc}')# % (threadName, exc))
			else:
				logging.info(f'({_serviceName}) - \'{threadName}\' finish without error and return \'{data}\'')

def hcsr04_pool(name, echo, trigger, pipeline):
	'''
	function loop for HC-SR04 sensor. 
	:params string name: name of the sensor
	:params int echo: location of the echo pin in the RPI
	:params int trigger: location of the trigger pin in the RPI
	:params queue pipeline: queue class for pushing data
	'''	
	#Initialize internal variable
	hcsr04 = None

	#Initializing Distance Sensor 
	logging.info(f'starting distance sensor {name} with HC-SR04 module at pins {echo}, {trigger}...')

	#If Internal debug is enable, generate random sensor value for testing purpose 
	#or instead start the sensor loop collection module
	if _isDebug:
		for _ in range(_debugIterAmount):
			sleep(_intervalMeasureTime)
			logging.debug(f'Internal-Debug-ON - reading sensor {name} value...')
			value = round(random.uniform(0.5, 2), 2)
			logging.debug(f'Internal-Debug-ON - queuing sensor {name} data values {value} cm...')
			pipeline['dist']['bus'].put((name, value))

	else:
		#hcsr04 = HCSR04(echo, trigger)
		while True:
			sleep(_intervalMeasureTime)
			logging.debug(f'reading sensor {name} value...')
			value = round(hcsr04.distance(), 2)
			logging.debug(f'queuing sensor {name} with value of {value}cm...')
			pipeline['dist']['bus'].put((name, value))