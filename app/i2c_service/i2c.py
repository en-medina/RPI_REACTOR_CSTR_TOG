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
    __internalLock = threading.Lock()

    def __init__(self,config):
        self.bus = smbus.SMBus(config['i2c']['channel'])
        self._internalDelay = 0.001

    def action(self, data):
        with self.__internalLock:
            sleep(self._internalDelay)
            print('start', data)
            ans = ''
            ans = [str(i) for i in range(data * 1, data * 10, data)]
            print(' '.join(ans))
            print('{} is finish'.format(data))

    def read_byte(self, address, register = None):
        with self.__internalLock:
            sleep(self._internalDelay)
            print('read_byte')
            self.bus.read_byte_data(address, register)
        pass

    def write_byte(self, address, msg, register = None):
        with self.__internalLock:
            sleep(self._internalDelay)
            print('write_byte')
            self.bus.write_byte_data(address, register, msg)
        pass

    def write_word_data(self, address, msg, register):
        with self.__internalLock:
            sleep(self._internalDelay)
            print('write_byte')
            self.bus.write_word_data(address, register, msg)
        pass

    def read_word_data(self, address, register):
        with self.__internalLock:
            sleep(self._internalDelay)
            print('read_word')
            return self.bus.read_word_data(address, register)
        pass

    def write_buffer(self, address, buffer, register):
        with self.__internalLock:
            for msg in buffer:
                self.bus.write_word_data(address, register, msg)
                pass
        pass


