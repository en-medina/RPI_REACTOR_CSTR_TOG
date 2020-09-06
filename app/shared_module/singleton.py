from threading import Lock

class Singleton(type):
	_instances = {}
	lock = Lock()

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			with cls.lock:
				if cls not in cls._instances:
					cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

class SingletonByArg(type):
	_instances = {}
	lock = Lock()

	def __call__(cls, *args, **kwargs):
		if (cls, args, tuple(kwargs)) not in cls._instances:
			with cls.lock:
				if (cls, args, tuple(kwargs)) not in cls._instances:
					cls._instances[(cls, args, tuple(kwargs))] = super(SingletonByArg, cls).__call__(*args, **kwargs)
		return cls._instances[(cls, args, tuple(kwargs))]


if __name__ == '__main__':
	class A(metaclass=SingletonByArg):
		def __init__(self, a, b):
			print(a,b)

	class B(metaclass=SingletonByArg):
		def __init__(self, a, b):
			print(a,b)

	a = A(1,2)
	b = A(1,2)
	c = A(2,1)
	d = B(2,1)
	print(a)
	print(b)
	print(c)
	print(d)
	pass
	
