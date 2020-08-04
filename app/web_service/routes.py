from flask import render_template, Flask, redirect, url_for
from flask_socketio import SocketIO
import shared_module.helpers as helpers
import logging
import shared_module.helpers as helpers
import shared_module.file_manager as file_manager
from .forms import LimitForm, GraphForm
from .graph import generate_graph
from json import loads as jsonloads, dumps as jsondumps
from datetime import datetime, timedelta

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
system_setting = file_manager.FileManager(helpers.abs_path('system_config.json', __file__))
pipeline = None

def run_flask(param):
	global pipeline
	logging.info(f'Starting Flask Framework Web Server...')

	app.config.update(dict(
    SECRET_KEY="WEFN ZLWLNDCOZL ASZ",
    WTF_CSRF_SECRET_KEY="HQIUNJOADBINLMFSDLVSX"	
  ))
	pipeline = param
	ipaddr = helpers.get_server_ip()
	socketio.run(app, host = ipaddr, debug = False)

@app.route("/")
def main_root():
	return redirect(url_for('index'))

@app.route("/index")
def index():
	ipaddr = helpers.get_server_ip()
	port = 5000
	return render_template('index.html', ipaddr = ipaddr, port = port)

@app.route("/about_us")
def about_us():
	return render_template('about_us.html')

@app.route("/configuration", methods=['POST', 'GET'])
def configuration():
	form = LimitForm()
	setting = system_setting.json2dict()
	ipaddr = helpers.get_server_ip()
	port = 5000
	if form.validate_on_submit():
		setting['threshold']['speed']['lo'] = form.loSpeed.data
		setting['threshold']['speed']['hi'] = form.hiSpeed.data
		setting['threshold']['temperature']['lo'] = form.loTemp.data
		setting['threshold']['temperature']['hi'] = form.hiTemp.data
		setting['threshold']['delay'] = form.delay.data
		system_setting.dict2json(setting)
		setting = system_setting.json2dict()
	return render_template('configuration.html', ipaddr = ipaddr, port = port, setting = setting, form=form)

@app.route("/graph", methods=['POST', 'GET'])
def graph():
	form = GraphForm()
	form.update_choices()

	graphData = {"data":[0],"labels":[0],"title":"Seleccione una gráfica"}  
	endTime = datetime.now()
	beginTime = endTime - timedelta(seconds=3600*2)
	interval = 900
	tableName = ''

	if form.validate_on_submit():
		beginTime = datetime.combine(form.beginDate.data, form.beginTime.data)
		endTime = datetime.combine(form.endDate.data, form.endTime.data)
		interval = int(form.intervalList.data)
		tableName = form.sensorList.data
		graphData = generate_graph(tableName, beginTime, endTime, interval)
		pass
	
	current={
		'beginDate': beginTime.strftime('%Y-%m-%d'),
		'beginTime':beginTime.strftime('%H:%M'),
		'endDate': endTime.strftime('%Y-%m-%d'),
		'endTime': endTime.strftime('%H:%M')
	}
	return render_template('graph.html', graphData=jsondumps(graphData), form=form, date=current, interval=interval, tableName=tableName)

@socketio.on('change_limit_state')
def change_limit_state(message):
	data = jsonloads(message)
	setting = system_setting.json2dict()
	setting['threshold']['state'] = int(data['state'])
	system_setting.dict2json(setting)
	setting = system_setting.json2dict()
	answer =  jsondumps({"state": setting['threshold']['state']})
	socketio.emit('update_limit_state', answer)

@socketio.on('change_system_state')
def change_system_state(message):
	global pipeline
	data = jsonloads(message)
	delay = float(data['delay'])
	state = bool(data['state'])
	pipeData = {
				'green':{'state':1,'delay':delay, 'reverse':False},
				'yellow':{'state':0, 'delay': delay, 'reverse':False},
				'alarm':{'state':0, 'delay': delay, 'reverse':False},
				'red':{'state':0,'delay':delay, 'reverse':False},
				'system':{'state':1,'delay':delay, 'reverse':False}
	}
	if not state:
		pipeData = {
				'green':{'state':0,'delay':delay, 'reverse':False},
				'yellow':{'state':0, 'delay': delay, 'reverse':False},
				'alarm':{'state':0, 'delay': delay, 'reverse':False},
				'red':{'state':1, 'delay':delay, 'reverse':False},
				'system':{'state':0, 'delay':delay, 'reverse':False}
			}
	pipeline['web']['bit'].put(pipeData)

	setting = system_setting.json2dict()
	setting['delay'] = delay
	system_setting.dict2json(setting)
	setting = system_setting.json2dict()
	response =  jsondumps({"state": int(state)})
	socketio.emit('update_system_state', response)
