#adc.py
#gy906.py
import logging
from time import sleep
import threading

try:
    import shared_module.singleton as singleton
except Exception:
    import importlib.util

    spec = importlib.util.spec_from_file_location("Singleton", "../shared_module/singleton.py")
    singleton = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(singleton)

try:
    import smbus
except Exception:
    logging.critical("smbus package not found...  creating None variable for testing purpose only...")
    smbus = None


class I2CIface(metaclass=singleton.Singleton):
    _internalLock = threading.Lock()

    def __init__(self,config):
        self.bus = smbus.SMBus(config['i2c']['channel'])
        self._internalDelay = 0.001

    def action(self, data):
        with self._internalLock:
            sleep(self._internalDelay)
            ans = ''
            ans = [str(i) for i in range(data * 1, data * 10, data)]

    def read_byte(self, address, register = None):
        with self._internalLock:
            sleep(self._internalDelay)
            self.bus.read_byte_data(address, register)
        pass

    def write_byte(self, address, msg, register = None):
        with self._internalLock:
            sleep(self._internalDelay)
            self.bus.write_byte_data(address, register, msg)
        pass

    def write_word_data(self, address, msg, register):
        with self._internalLock:
            sleep(self._internalDelay)
            self.bus.write_word_data(address, register, msg)
        pass

    def read_word_data(self, address, register):
        with self._internalLock:
            sleep(self._internalDelay)
            return self.bus.read_word_data(address, register)
        pass

    def write_i2c_block_data(self, address, buff, register):
        #buffer is a list
        with self._internalLock:
            sleep(self._internalDelay)
            self.bus.write_i2c_block_data(address, register, buff)

    def read_i2c_block_data(address,  register, block=2):
        with self._internalLock:
            sleep(self._internalDelay)
            return self.bus.read_i2c_block_data(address, register, block)



