import importlib.util
from time import sleep
# import board
# import busio
# import adafruit_ads1x15.ads1115 as ADS
# from adafruit_ads1x15.analog_in import AnalogIn
spec = importlib.util.spec_from_file_location("i2c", "../i2c_service/i2c.py")
i2c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(i2c)

spec = importlib.util.spec_from_file_location("AnalogIn, ADS1115", "../i2c_service/ads1115.py")
adc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adc)



if '__main__' == __name__:
	channel = 1
	i2cIface = i2c.I2CIface(channel)
	adc_reader = adc.ADS1115(i2cIface)
	channels = [adc.AnalogIn(adc_reader, 0),
		adc.AnalogIn(adc_reader, 1),
		adc.AnalogIn(adc_reader, 2),
		adc.AnalogIn(adc_reader, 3)]
	while True:
		for i in range(len(channels)):
			print('In the channel', i, 'the value is:', channels[i].value)
			sleep(2)
		print('\n\n')