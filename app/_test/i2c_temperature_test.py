import importlib.util
from time import sleep
spec = importlib.util.spec_from_file_location("i2c", "../i2c_service/i2c.py")
i2c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(i2c)

spec = importlib.util.spec_from_file_location("MLX90614", "../i2c_service/mlx90614.py")
mlx90614 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mlx90614)

if '__main__' == __name__:
	channel = 1
	i2cIface = i2c.I2CIface(channel)
	temperature = [
		(0x5a, mlx90614.MLX90614(i2cIface, 'reactive1_temperature', 0x5a)),
		(0x5b, mlx90614.MLX90614(i2cIface, 'reactive1_temperature', 0x5b)),
		(0x5c, mlx90614.MLX90614(i2cIface, 'reactive1_temperature', 0x5c))]
	while True:
		for i in range(len(temperature)):
			print('the temperature of the sensor',temperature[i][0],'is',temperature[i][1].get_object_1(),'Celcius')
			sleep(1)
		print('\n\n')