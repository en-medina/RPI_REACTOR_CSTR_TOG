import threading
import concurrent.futures
from .i2c import I2CIface
#from .Ghelpers import json2dict, str2hex
import shared_module.helpers as helpers
from .mlx90614 import MLX90614
from time import sleep
import logging 
import random

#from .ads1115 import ADS, AnalogIn

_intervalMeasureTime = float()
_startLoop = bool()
_isDebug = bool()
_debugIterAmount = int()
_serviceName = str()


def init_i2c(pipeline):
	'''
	function for initialize and run I2C module and sensors
	:param queue pipeline: queue class for pushing data
	'''
	logging.info('Starting I2C Service...')

	global _isDebug, _startLoop, _intervalMeasureTime, _debugIterAmount, _serviceName 

	config = helpers.json2dict('config.json', __file__)
	_intervalMeasureTime = config['i2c']['intervaltime']
	_startLoop = config['i2c']['loop']
	_isDebug = config['i2c']['debug']
	_debugIterAmount = config['i2c']['iter']
	_serviceName = config['i2c']['threadname']

	if _isDebug:
		logging.warning(f'({_serviceName}) - internal debug is enable...')

	temp_params = [
		{
			'name': name, 
			'addr': addr, 
			'pipeline': pipeline,
			'channel': config['i2c']['channel']
		} 
		for name, addr in config['i2c']['address'].items() if 'adc' not in name
	]

	adc_params = {
			'name': 'adc-service',
			'addr': config['i2c']['address']['adc'],
			'pipeline': pipeline,
			'adc': config['adc'],
			'channel': config['i2c']['channel']
	}

	with concurrent.futures.ThreadPoolExecutor(max_workers=3, thread_name_prefix = _serviceName) as executor:

		futureException = {
			executor.submit(mlx90614_loop, data): data['name'] for data in temp_params
		}
		futureException[executor.submit(adc1115_loop, adc_params)] = adc_params['name']

		for futureErrors in concurrent.futures.as_completed(futureException):
			threadName = futureException[futureErrors]
			try:
				data = futureErrors.result()
			except Exception as exc:
				logging.error(f'({_serviceName}) - \'{threadName}\' generated an exception: {exc}')# % (threadName, exc))
			else:
				logging.info(f'({_serviceName}) - \'{threadName}\' finish without error and return \'{data}\'')


def mlx90614_loop(params):
	'''
	function loop for mlx90614 sensor. 
	:params dict params: init value of the sensor name, address and pipeline
	'''
	#Initialize internal variable
	name	= params['name']
	address	= params['addr']
	pipeline = params['pipeline']
	channel = params['channel']
	sensor = None

	#Initializing Temperature Sensor 
	logging.info(f'starting temperature sensor {name} with MLX90614 module at address {address}...')
	#If Internal debug is enable, generate random sensor value for testing purpose 
	#or instead start the sensor loop collection module
	if _isDebug:
		for _ in range(_debugIterAmount):
			_debug_collect_sensor_data(name, random.uniform(16, 100), pipeline)
	
	#Start the sensor loop collection module
	else:
		#Initializing Temperature Sensor 
		sensor = MLX90614(I2CIface(channel), name, address=helpers.str2hex(address))

		#Collect data of the sensor	in a undefined matter
		while _startLoop:
			_collect_sensor_data(sensor, pipeline)


def adc1115_loop(params):
	'''
	function loop for ADS1115 chip. 
	:params dict params: init value of the sensor name, address and pipeline
	'''

	#Initialize internal variable
	name	= params['name']
	address	= params['addr']
	pipeline = params['pipeline']
	config = params['adc']
	channel = params['channel']
	ads = None
	sensors = list()

	#Initializing ADC module if not internal debug mode is enable
	logging.info(f'starting ADC1115 module at address {address}...')
	if not _isDebug:
		ads = adc.ADS1115(i2cIface(channel), address=helpers.str2hex(address))

	#If Internal debug is enable, generate random sensor value for testing purpose 
	#or instead initiziale each sensor analog input and start the sensor loop collection module
	devices_name = config['selector'].keys()
	logging.info(f'starting ADC1115 devices {list(devices_name)}...')
	if _isDebug:
		for _ in range(_debugIterAmount):
			for name in devices_name:
				_debug_collect_sensor_data(name, random.uniform(1, 10), pipeline)

	#initiziale each sensor analog input and start the sensor loop collection module
	else:
		sensors = [AnalogIn(ads, config['selector'][name]['pin'], 
			name,config['selector'][name]['slope'],config['selector'][name]['offset']
			) for name in devices_name]		
		while _startLoop:
			for sensor in sensors:	
				_collect_sensor_data(sensor, pipeline)


def _collect_sensor_data(sensor, pipeline):
	'''
	internal function for collecting the sensor data and push it 
	to the parent pipeline
	:param AnalogIn/MLX90614 sensor: it may be MLX90614 or AnalogIn class
	:param queue pipeline: queue class for pushing data
	'''
	sleep(_intervalMeasureTime)
	logging.debug(f'reading sensor {sensor.name} value...')
	value = round(sensor.value, 2)
	logging.debug(f'queuing sensor {sensor.name} with value of {value:.2f}...')
	pipeline['i2c']['bus'].put((sensor.name, value))


def _debug_collect_sensor_data(name, value, pipeline):
	'''
	internal function for simulated sensor data collection and push it 
	to the parent pipeline
	:param string name: sensor name
	:param float value: sensor value
	:param queue pipeline: queue class for pushing data
	'''
	sleep(_intervalMeasureTime)
	value = round(value, 2)
	logging.debug(f'Internal-Debug-ON - reading sensor {name} value...')
	logging.debug(f'queuing sensor {name} with value of {value} Celcius...')
	pipeline['i2c']['bus'].put((name, value))

