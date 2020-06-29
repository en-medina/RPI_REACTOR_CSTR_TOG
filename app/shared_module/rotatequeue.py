from collections import deque

class RotateQueue():
	
	def __init__(self, maxlen=None):
		self._queue = deque(maxlen=maxlen)

	def empty(self):
		return len(self._queue) == 0

	def put(self, data):
		self._queue.appendleft(data)

	def get(self):
		return self._queue.pop()