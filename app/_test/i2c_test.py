import importlib.util

spec = importlib.util.spec_from_file_location("i2c", "../i2c_service/i2c.py")
i2c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(i2c)

spec = importlib.util.spec_from_file_location("MLX90614", "../i2c_service/mlx90614.py")
mlx90614 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mlx90614)

if '__main__' == __name__:
	config = {'i2c':{'channel':1}}
	i2cIface = i2c.I2CIface(config)
	temperature1 = mlx90614.MLX90614(i2cIface, 'reactive1_temperature', 0x5b)
	for _ in range(10):
		print('the temperature is:', temperature1.get_ambient())