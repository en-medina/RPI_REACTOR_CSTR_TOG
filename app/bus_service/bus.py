from time import sleep
import logging
import concurrent.futures
import shared_module.helpers as helpers
import shared_module.database as database

_intervalMeasureTime = float()
_startLoop = bool()
_isDebug = bool()
_debugIterAmount = int()
_serviceName = str()
_serviceDB = None


def init_bus(pipeline, deviceNames):
	
	logging.info('Starting BUS service...')

	global _isDebug, _startLoop, _intervalMeasureTime, _debugIterAmount, _serviceName, _serviceDB
	config = helpers.json2dict('config.json', __file__)
	_intervalMeasureTime = config['bus']['intervaltime']
	_startLoop = config['bus']['loop']
	_isDebug = config['bus']['debug']
	_debugIterAmount = config['bus']['iter']
	_serviceName = config['bus']['threadname']

	if _isDebug:
		logging.warning(f'({_serviceName}) - internal debug is enable...')

	
	logging.info(f'({_serviceName}) - starting Database...')

	Names = list()
	for value in deviceNames.values():
		Names.extend(value)
	_serviceDB = database.SQLITE(tableName = Names)
	deviceNames = Names
	logging.info(_serviceDB.get_table_name())

	with concurrent.futures.ThreadPoolExecutor(max_workers=3, thread_name_prefix = _serviceName) as executor:
		futureException = {
			executor.submit(push_data, _queue): 
			f'{name}-collector' for name, _queue in zip(['i2c','bus'], [pipeline['i2c']['bus'], pipeline['dist']['bus']])
		}

		for futureErrors in concurrent.futures.as_completed(futureException):
			threadName = futureException[futureErrors]
			try:
				data = futureErrors.result()
			except Exception as exc:
				logging.error(f'({_serviceName}) - \'{threadName}\' generated an exception: {exc}')
			else:
				logging.info(f'({_serviceName}) - \'{threadName}\' finish without error and return \'{data}\'')

	if _isDebug:
		for name in deviceNames:
			data = _serviceDB.get_values(name)
			logging.info(f'({_serviceName}) - \'{threadName}\' retriving data from {name} and have {data}')

def push_data(_queue):
	if _isDebug:
		_debug_push_data(_queue)
	else:
		while True:
			while not _queue.empty():
				data = _queue.get()
				logging.debug(f'from device {data[0]} was get the value {data[1]}, pushing to {data[0]} table...')
				_serviceDB.insert(*data)
				sleep(_intervalMeasureTime)

def _debug_push_data(_queue):
	for _ in range(_debugIterAmount):
		while not _queue.empty():
			data = _queue.get()
			logging.info(f'from device {data[0]} was get the value {data[1]}, pushing to {data[0]} table...')
			print(data)
			_serviceDB.insert(*data)
			sleep(_intervalMeasureTime)

