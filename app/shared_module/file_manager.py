from threading import Lock
from json import loads as jloads, dumps as jdumps
from .singleton import SingletonByArg


class FileManager(metaclass=SingletonByArg):

	def __init__(self, filename):
		self.filename = filename
		self.lock = Lock()
		open(filename,'a').close()

	def __str__(self):
		return self.filename

	def txt2list(self):
		with self.lock:
			with open(self.filename) as rawInfo:
				lines = rawInfo.readlines()
				return lines.strip('\n')

	def json2dict(self):
		with self.lock:
			with open(self.filename) as rawInfo:
				lines = rawInfo.read()
				return jloads(lines)

	def list2txt(self, data, mode='w'):
		with self.lock:
			with open(self.filename, mode) as rawFile:
				rawFile.write('\n' + '\n'.join(data))

	def dict2json(self, data):
		with self.lock:
			data = jdumps(data)
			with open(self.filename, 'w') as rawFile:
				rawFile.write(data)
