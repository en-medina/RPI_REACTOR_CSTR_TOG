#adc.py
#gy906.py

from time import sleep
#import smbus
import threading
import shared_module.singleton as singleton


class I2CIface(metaclass=singleton.Singleton):
    #bus = smbus.SMBus(config['i2c']['channel'])
    __internalLock = threading.Lock()
    __internalDelay = 0.001
    def action(self, data):
        with self.__internalLock:
            sleep(__internalDelay)
            print('start', data)
            ans = ''
            ans = [str(i) for i in range(data * 1, data * 10, data)]
            print(' '.join(ans))
            print('{} is finish'.format(data))

    def read_byte(self, address, register = None):
        with self.__internalLock:
            sleep(__internalDelay)
            print('read_byte')
            #self.bus.read_i2c_block_data(address, register)
        pass

    def write_byte(self, address, msg, register = None):
        with self.__internalLock:
            sleep(__internalDelay)
            print('write_byte')
            #self.bus.write_i2c_block_data(address, register, msg)
        pass

    def write_word_data(self, address, msg, register):
        with self.__internalLock:
            sleep(__internalDelay)
            print('write_byte')
            #self.bus.write_word_data(address, register, msg)
        pass
    def write_buffer(self, address, buffer, register):
        with self.__internalLock:
            for msg in buffer:
                #self.bus.write_word_data(address, register, msg)
                pass
        pass

    def read_word_data(self, address, register):
        with self.__internalLock:
            sleep(__internalDelay)
            print('read_word')
            #return self.bus.read_word_data(address, register)
        pass

