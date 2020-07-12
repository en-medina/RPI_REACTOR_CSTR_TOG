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

def run_flask():
	logging.info(f'Starting Flask Framework Web Server...')

	app.config.update(dict(
    SECRET_KEY="WEFN ZLWLNDCOZL ASZ",
    WTF_CSRF_SECRET_KEY="HQIUNJOADBINLMFSDLVSX"	
  ))
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
		system_setting.dict2json(setting)
		setting = system_setting.json2dict()
	return render_template('configuration.html', ipaddr = ipaddr, port = port, setting = setting, form=form)

@app.route("/graph", methods=['POST', 'GET'])
def graph():
	form = GraphForm()
	form.update_choices()
	#graphData = {"data":[1,2,1,1,5,3,0,7],"labels":[1,2,3,4,5,6,7,8],"title":"my Line"} 
	graphData = {"data":[0],"labels":[0],"title":"Seleccione una gráfica"}  
	if form.validate_on_submit():
		beginTime = datetime.combine(form.beginDate.data, form.beginTime.data)
		endTime = datetime.combine(form.endDate.data, form.endTime.data)
		interval = int(form.intervalList.data)
		tableName = form.sensorList.data
		graphData = generate_graph(tableName, beginTime, endTime, interval)
		pass
	
	current_time = datetime.now()
	current={
		'beginDate': (current_time - timedelta(seconds=3600*2)).strftime('%Y-%m-%d'),
		'beginTime':(current_time - timedelta(seconds=3600*2)).strftime('%H:%M'),
		'endDate': current_time.strftime('%Y-%m-%d'),
		'endTime': current_time.strftime('%H:%M')
	}
	return render_template('graph.html', graphData=jsondumps(graphData), form=form, date=current)

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
	data = jsonloads(message)
	state = bool(message['state'])
	delay = int(message['delay'])
