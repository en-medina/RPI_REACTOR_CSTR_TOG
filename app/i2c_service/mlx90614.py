"""
MIT License

Copyright (c) 2016 Arsenijs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#The original version of this library was written by SFXRescue
#Please find below it's github's repository
#https://github.com/SFXRescue/PyMLX90614

from time import sleep

class MLX90614():

    # RAM offsets with 16-bit data, MSB first
    # Raw data IR channel 1
    MLX90614_RAWIR1 = 0x04
    # Raw data IR channel 2
    MLX90614_RAWIR2 = 0x05
    # Ambient temperature
    MLX90614_TA = 0x06
    # Object 1 temperature
    MLX90614_TOBJ1 = 0x07
    # Object 2 temperature
    MLX90614_TOBJ2 = 0x08

    # EEPROM offsets with 16-bit data, MSB first
    # Object temperature max register
    MLX90614_TOMAX = 0x20
    # Object temperature min register
    MLX90614_TOMIN = 0x21
    # PWM configuration register
    MLX90614_PWMCTRL = 0x22
    # Ambient temperature register
    MLX90614_TARANGE = 0x23
    # Emissivity correction register
    MLX90614_EMISS = 0x24
    # Configuration register
    MLX90614_CONFIG = 0x25
    # Slave address register
    MLX90614_ADDR = 0x2E
    # 1 ID register (read-only)
    MLX90614_ID1 = 0x3C
    # 2 ID register (read-only)
    MLX90614_ID2 = 0x3D
    # 3 ID register (read-only)
    MLX90614_ID3 = 0x3E
    # 4 ID register (read-only)
    MLX90614_ID4 = 0x3F

    comm_retries = 5
    comm_sleep_amount = 0.1

    def __init__(self, bus, name, address=0x5A):
        self.bus = bus
        self.address = address
        self._name = name

    def read_reg(self, reg_addr):
        err = None
        for i in range(self.comm_retries):
            try:
                return self.bus.read_word_data(self.address, reg_addr)
            except IOError as e:
                err = e
                # "Rate limiting" - sleeping to prevent problems with sensor
                # when requesting data too quickly
                sleep(self.comm_sleep_amount)
        # By this time, we made a couple requests and the sensor didn't respond
        # (judging by the fact we haven't returned from this function yet)
        # So let's just re-raise the last IOError we got
        raise err

    def read_temp(self, reg):
        data = self.read_reg(reg)
        temp = (data * 0.02) - 273.15
        return round(temp, 2)

    @property
    def measure(self):
        return 'Celcius'

    @property
    def name(self):
        return self._name
    
    @property
    def value(self):
        return self.get_object_1()

    def get_ambient(self):
        return self.read_temp(self.MLX90614_TA)

    def get_object_1(self):
        return self.read_temp(self.MLX90614_TOBJ1)

    def get_object_2(self):
        return self.read_temp(self.MLX90614_TOBJ2)

