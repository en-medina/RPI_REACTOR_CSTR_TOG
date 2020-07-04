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
	config = {'i2c':{'channel':1}}
	i2cIface = i2c.I2CIface(config)
	adc_reader = adc.ADS1115(i2cIface)
	channel = adc.AnalogIn(adc_reader, 0)
	voltage = 0
	value = 0
	n = 100
	for _ in range(n):
		voltage += channel.voltage
		value += channel.value
		#sleep(0.001)
	voltage = voltage/n
	value = value/n
	print('the value is:', value, 'the voltage is:', voltage)
