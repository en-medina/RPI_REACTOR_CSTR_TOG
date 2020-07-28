#from .hcsr04 import HCSR04
import concurrent.futures
import shared_module.helpers as helpers
from time import sleep
import logging 
import random
from .bit_controller import BitController
try:
	import RPi.GPIO as GPIO
	#GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
except Exception:
    logging.critical("RPi.GPIO package not found... creating None variable for testing purpose only...")
    GPIO = None
_intervalMeasureTime = float()
_startLoop = bool()
_isDebug = bool()
_debugIterAmount = int()
_serviceName = str()

def init_bit(pipeline):
	'''
	function for initialize and run BIT module
	:param queue pipeline: queue class for pushing data
	'''
	logging.info('Starting BIT Service...')

	global _isDebug, _startLoop, _intervalMeasureTime, _debugIterAmount, _serviceName

	#Check if GPIO library exist, if not, return
	if GPIO is None:
		return

	config = helpers.json2dict('config.json', __file__)
	_intervalMeasureTime = config['bit']['intervaltime']
	_startLoop = config['bit']['loop']
	_isDebug = config['bit']['debug']
	_debugIterAmount = config['bit']['iter']
	_serviceName = config['bit']['threadname']

	if _isDebug:
		logging.warning(f'({_serviceName}) - internal debug is enable...')

	bitControllerDict = {
		key: BitController(value, config['bit']['state'][key]) for key, value in config['bit']['pinout'].items()
	}

	with concurrent.futures.ThreadPoolExecutor(max_workers=3, thread_name_prefix = _serviceName) as executor:

		futureException = {
			executor.submit(
				bit_state_supervisor, bitController
				): key + '_bit_state_supervisor' for key, bitController in bitControllerDict.items()
		}
		futureException.update({
			executor.submit(update_state_monitor, pipeline, bitControllerDict):'update_state_monitor',
			executor.submit(notify_bit_state, pipeline, bitControllerDict):'notify_bit_state'
			})

		for futureErrors in concurrent.futures.as_completed(futureException):
			threadName = futureException[futureErrors]
			try:
				data = futureErrors.result()
			except Exception as exc:
				logging.error(f'({_serviceName}) - \'{threadName}\' generated an exception: {exc}')
			else:
				logging.info(f'({_serviceName}) - \'{threadName}\' finish without error and return \'{data}\'')

def notify_bit_state(pipeline, bitControllerDict):
	'''
	function loop for notify the state of the IO bit output devices
	:params dict(dict(queue)) pipeline: queue class dict for pushing data
	:params dict(BitController) bitControllerDict: Dictionary containing bit controller class
	'''	
	logging.info(f'Starting notify_bit_state module...')
	while True:
		pipeline['bit']['web'].put({
			'state':{
				name: bitController.state
				for name, bitController in bitControllerDict.items()
			}
		})
		sleep(_intervalMeasureTime)

def update_state_monitor(pipeline, bitControllerDict):
	'''
	function loop for monitor Updates for the IO bit output devices
	:params dict(dict(queue)) pipeline: queue class dict for pushing data
	:params dict(BitController) bitControllerDict: Dictionary containing bit controller class
	'''	
	logging.info(f'Starting update_state_monitor module...')
	while True:
		while not pipeline['web']['bit'].empty():
			futureState = pipeline['web']['bit'].pop()
			for key in futureState.keys():
				bitControllerDict[key].notify_change(
					futureState[key]['state'], 
					futureState[key]['delay'], 
					futureState[key]['reverse'])
		sleep(_intervalMeasureTime)

def bit_state_supervisor(bitController):
	'''
	function loop for change a signle IO bit output devices
	:params BitController bitController:  bit controller class
	'''	
	logging.info(f'Starting bit controller module located at pin {bitController}...')
	while True:
		while bitController.notification:
			sleep(bitController.delay)
			bitController.apply_change()
		sleep(_intervalMeasureTime)