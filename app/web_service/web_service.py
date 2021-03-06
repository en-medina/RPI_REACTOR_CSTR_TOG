from flask import Flask

from queue import Queue
from time import sleep
from .routes import socketio, run_flask


import logging
import shared_module.helpers as helpers
import shared_module.database as database
import shared_module.file_manager as file_manager
import concurrent.futures
from json import dumps as jsondumps

logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)

_intervalMeasureTime = float()
_startLoop = bool()
_isDebug = bool()
_debugIterAmount = int()
_serviceName = str()


def init_web(pipeline):
	'''
	This function is in charge of initialize, running and coordinate all the threads related to web server interaction.

	:param dict(dict(RotateQueue)) pipeline: communication pipeline hierarchy 
	'''

	logging.info('Starting WEB service...')

	global _isDebug, _startLoop, _intervalMeasureTime, _debugIterAmount, _serviceName

	config = helpers.json2dict('config.json', __file__)
	_serviceName = config['web']['threadname']
	_isDebug = config['web']['debug']
	_debugIterAmount = config['web']['iter']
	_intervalMeasureTime = config['web']['intervaltime']
	internalPipeline ={
		'websocket': Queue(),
		'monitor': Queue()
	}

	with concurrent.futures.ThreadPoolExecutor(max_workers=5, thread_name_prefix = _serviceName) as executor:

		futureException = {
			executor.submit(web_server, pipeline): 'flask_service',
			executor.submit(system_information, internalPipeline): 'system_information',
			executor.submit(system_monitor, internalPipeline, pipeline, 'monitor'): 'system_monitor',
			executor.submit(web_emit_system_info, internalPipeline, 'websocket'): 'web_emit_system_info',
			executor.submit(web_emit_system_state, pipeline): 'web_emit_system_state'
		}

		for futureErrors in concurrent.futures.as_completed(futureException):
			threadName = futureException[futureErrors]
			try:
				data = futureErrors.result()
			except Exception as exc:
				logging.error(f'({_serviceName}) - \'{threadName}\' generated an exception: {exc}')
			else:
				logging.info(f'({_serviceName}) - \'{threadName}\' finish without error and return \'{data}\'')

def web_server(pipeline):
	'''
	This function is for starting flask server.

	:param dict(dict(RotateQueue)) pipeline: communication pipeline hierarchy 
	'''
	run_flask(pipeline)

def system_information(internalPipeline):
	'''
	This function is for collecting data from the database and push it to internal web server pipeline.

	:param dict(RotateQueue) internalPipeline: internal communication pipeline hierarchy 
	'''

	logging.info(f'Starting System Information Poller...')
	db = database.SQLITE()
	icnt = 0
	while True and (not _isDebug or icnt <= _debugIterAmount):
		data = dict()
		sleep(_intervalMeasureTime)
		icnt += 1

		for table in db.get_table_name():
			data[table] = db.get_last_value(table)

		logging.debug(f'System Information collect data from {len(data)} tables')
		for key in internalPipeline.keys():
			if len(data) != 0:
				internalPipeline[key].put(data)

def evaluate_threshold(limit, value, delay, pipeline):
	'''
	This function is evaluating the threshold parameters with the sensors current value.

	:param dict(float) limit: threshold value
	:param float value: sensor current value
	:param float delay: delay of the next state change
	:param dict(dict(RotateQueue)) pipeline: communication pipeline hierarchy

	:return bool: return true if value is under the defined bound or instead return false.
	'''
	if not limit['lo'] <= value <= limit['hi']:
		if delay != 0:
			pipeline['web']['bit'].put(
				{
					'green':{'state':0,'delay':0, 'reverse':False},
					'yellow':{'state':1, 'delay': delay, 'reverse':True},
					'alarm':{'state':1, 'delay': delay, 'reverse':True},
					'red':{'state':1,'delay':delay, 'reverse':False},
					'system':{'state':0,'delay':delay, 'reverse':False}
				}
			)
		else:
			pipeline['web']['bit'].put(
				{
					'green':{'state':0,'delay':0, 'reverse':False},
					'yellow':{'state':0, 'delay': 0, 'reverse':False},
					'alarm':{'state':0, 'delay': 0, 'reverse':False},
					'red':{'state':1, 'delay':0, 'reverse':False},
					'system':{'state':0, 'delay':0, 'reverse':False}
				}
			)
		return False
	return True


def system_monitor(internalPipeline, pipeline, monitorKey):
	'''
	This function is for monitor the value of each sensor in order to take action if break the defined bound limits.

	:param dict(RotateQueue) internalPipeline: internal communication pipeline hierarchy 
	:param dict(dict(RotateQueue)) pipeline: communication pipeline hierarchy
	:param string monitorKey: internal monitor key to access the internal pipeline
	'''

	logging.info(f'Starting System Threshold Monitor...')
	system_setting = file_manager.FileManager(helpers.abs_path('system_config.json', __file__))
	icnt = 0
	while True and (not _isDebug or icnt <= _debugIterAmount):

		# Debug Forced delay Implementation
		icnt += 1
		sleep(_intervalMeasureTime)

		while not internalPipeline[monitorKey].empty():
			data = internalPipeline[monitorKey].get()
			limits = system_setting.json2dict()
			isInSafeState = True
			if limits['threshold']['state']:
				for key, value in data.items():
					if 'temperature' in key:
						isInSafeState &= evaluate_threshold(limits['threshold']['temperature'], value[0], limits['threshold']['delay'], pipeline)
					# elif 'speed' in key:
					# 	isInSafeState &= evaluate_threshold(limits['threshold']['speed'], value[0], limits['threshold']['delay'], pipeline)

def web_emit_system_info(internalPipeline, broadcastKey):
	'''
	This function is for pushing current value of each sensor to the user using websocket

	:param dict(RotateQueue) internalPipeline: internal communication pipeline hierarchy 
	:param string broadcastKey: internal broadcast key to access the internal pipeline
	'''
	logging.info(f'Starting Web Socket System Information Module...')
	icnt = 0
	while True  and (not _isDebug or icnt <= _debugIterAmount):

		# Debug Forced delay Implementation
		icnt += 1
		sleep(_intervalMeasureTime)

		while not internalPipeline[broadcastKey].empty():
			data = internalPipeline[broadcastKey].get()
			data = jsondumps(data, default = helpers.datetime2str)
			socketio.emit('update_information', data, broadcast=True)


def web_emit_system_state(pipeline):
	'''
	This function is for pushing current system state of the system to the user

	:param dict(dict(RotateQueue)) pipeline: communication pipeline hierarchy
	'''
	logging.info(f'Starting Web Socket System State Module...')
	icnt = 0
	while True and (not _isDebug or icnt <= _debugIterAmount):
		icnt += 1
		sleep(_intervalMeasureTime)
		while not pipeline['bit']['web'].empty():
			data = pipeline['bit']['web'].get()
			response =  jsondumps({"state": int(data['state']['system'])})
			socketio.emit('update_system_state', response)
			
	pass