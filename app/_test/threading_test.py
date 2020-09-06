from flask import Flask, request
from time import sleep
from random import randint, uniform
from threading import Thread, Lock
from queue	import Queue

def create_cloud_resource(id, answer):
	sleep(10)
	answer.put(uniform(-1, -100))

class ThreadDict():
	_lock = Lock()
	_state_db = dict()

	def launch_process(self,userID):
		with self._lock:
			self._state_db[userID] = dict()
			self._state_db[userID]['answer'] = Queue()
			self._state_db[userID]['thread'] = Thread(target = create_cloud_resource, args=(userID, self._state_db[userID]['answer']))
			self._state_db[userID]['thread'].start()

	def _is_finish(self, userID):
		try:
			return not self._state_db[userID]['answer'].empty()
		except Exception as e:
			return None

	def is_ready(self, userID):
		with self._lock:
			return self._is_finish(userID)

	def get_answer(self, userID):
		with self._lock:
			if self._is_finish(userID):
				answer = self._state_db[userID]['answer'].get()
				self._state_db.pop(userID)
				return answer	
			return None

app = Flask(__name__)
state_db = ThreadDict()

@app.route('/launch')
def launch_resource():
	userID = randint(1000, 2000)
	state_db.launch_process(userID)
	print(userID)
	return f'Your userID is {userID}, and your request is in process'

@app.route('/check')
def check_resource():
	userID = int(request.args['id'])
	state = state_db.is_ready(userID) 
	print(userID, state)
	if state is True:
		answer = state_db.get_answer(userID)
		return f'Hi {userID} your process is finish and the answer is {answer}'
	elif state is False:
		return f'Hi {userID}, we are working on your process'
	return f'Hi userID do not found, please create a request'


if __name__ == '__main__':
	app.run(threaded = True, debug = False)		