from flask import render_template, Flask, redirect, url_for
from flask_socketio import SocketIO
import shared_module.helpers as helpers
import logging
import shared_module.helpers as helpers
import shared_module.file_manager as file_manager
from .forms import LimitForm
from json import loads as jsonloads, dumps as jsondumps

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
system_setting = file_manager.FileManager(helpers.abs_path('system_config.json', __file__))

def run_flask():
	logging.info(f'Starting Flask Framework Web Server...')

	app.config.update(dict(
    SECRET_KEY="my secret key",
    WTF_CSRF_SECRET_KEY="my csrf secret key"	
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
