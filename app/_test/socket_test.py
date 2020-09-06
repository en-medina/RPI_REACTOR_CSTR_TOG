      
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import logging
import random
from time import sleep
import threading
from os import path

app = Flask(__name__, template_folder=path.dirname(__file__))
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins="*")

@socketio.on('connect')                          
def test_connect():                        
	logging.info(f'Client connected')
	emit('my response', {'data': 'Connected'})

@app.route('/')
def index():
	return render_template('socket.html')

@socketio.on('my event')                          
def test_message(message):                        
	logging.info(f'The received Message is: {message}')
	emit('my response', {'data': 'got it!'})      


def my_thread(countDown):
	for _ in range(countDown):
		logging.info('Generating new number...')
		num = random.randint(0,100)
		socketio.emit('new data', f'The server generated for you the value {num}', broadcast=True)
		sleep(1)


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO,
	format='[%(levelname)s] %(message)s'
	)
	t = threading.Thread(target=my_thread, args=(100,))
	t.start()
	socketio.run(app)