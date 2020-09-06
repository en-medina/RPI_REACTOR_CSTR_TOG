
import logging
from time import sleep
import threading
import shared_module.singleton as singleton

#Try the importation of the SMBus Module
#if the module does not find in the interpreter
#launch a log message and intialize a None variable
#with the module name
try:
	import smbus
except Exception:
	logging.critical("smbus package not found...  creating None variable for testing purpose only...")
	smbus = None


class I2CIface(metaclass=singleton.Singleton):
	__internalLock = threading.Lock()

	def __init__(self, channel=1):
		"""
		This class contain the library for interfacing with the I2C protocol message. Also, handle the communication from multiple threads with any I2C device connected to this single I2C channel on the system. 

		:param int channel: the channel where is located the I2C port, take in note that have a default value of 1.
		"""

		#Initiliaze the variables
		self.bus = smbus.SMBus(channel)
		self._internalDelay = 0.001

	def read_byte(self, address, register = None):
		"""
		Read a byte from register of device located at the indicated address.
		
		:param int address: i2c address of the device.
		:param int register: space location that holds the data. the default value is None.

		:return int: bytes read from the device
		"""
		with self.__internalLock:
			sleep(self._internalDelay)
			return self.bus.read_byte_data(address, register)
		pass

	def write_byte(self, address, msg, register = None):
		"""
		write a byte to register of device located at the indicated address.
		
		:param int address: i2c address of the device.
		:param int msg: message that will be write in the device.
		:param int register: space location that holds the data. the default value is None.

		:return None:
		"""

		with self.__internalLock:
			sleep(self._internalDelay)
			self.bus.write_byte_data(address, register, msg)
		pass

	def write_word_data(self, address, msg, register):
		"""
		write a word to register of device located at the indicated address.
		
		:param int address: i2c address of the device.
		:param int msg: message that will be written in the device.
		:param int register: space location that holds the data. the default value is None.

		:return None:
		"""

		with self.__internalLock:
			sleep(self._internalDelay)
			self.bus.write_word_data(address, register, msg)
		pass

	def read_word_data(self, address, register):
		"""
		read a word from register of device located at the indicated address.
		
		:param int address: i2c address of the device.
		:param int register: space location that holds the data. the default value is None.

		:return int: word read from the device
		"""

		with self.__internalLock:
			sleep(self._internalDelay)
			return self.bus.read_word_data(address, register)
		pass

	def write_i2c_block_data(self, address, buff, register):
		"""
		write a word to register of device located at the indicated address.
		
		:param int address: i2c address of the device.
		:param list(int) buffer: a list of values that will be written in the device.
		:param int register: space location that holds the data. the default value is None.

		:return None:
		"""
		#buffer is a list
		with self.__internalLock:
			sleep(self._internalDelay)
			self.bus.write_i2c_block_data(address, register, buff)

	def read_i2c_block_data(self, address,  register, block=2):
		"""
		read a word from register of device located at the indicated address.
		
		:param int address: i2c address of the device.
		:param int register: space location that holds the data. the default value is None.

		:return int: word read from the device
		"""

		with self.__internalLock:
			sleep(self._internalDelay)
			return self.bus.read_i2c_block_data(address, register, block)

