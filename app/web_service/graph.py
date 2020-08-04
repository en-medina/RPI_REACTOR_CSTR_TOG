import shared_module.database as database
from datetime import timedelta
from functools import reduce


def generate_graph(tableName, beginDate, endDate, interval=60):
	db = database.SQLITE()
	names = {
			"reactive1_volume":"Volumen Tanque 1",
			"reactive2_volume":"Volumen Tanque 2",
			"reactive1_temperature":"Temperatura Reactivo 1",
			"reactive2_temperature":"Temperatura Reactivo 2",
			"reactor_temperature":"Temperatura en el Reactor",
			"reactive2_flow":"Caudal Reactivo 2",
			"reactive1_flow":"Caudal Reactivo 1",
			"agitator_speed": "Velocidad Agitador"
		}
	graph = {
		'title':names[tableName],
		'data':list(),
		'labels':list()
	}

	iterDate = beginDate
	increment = timedelta(seconds=interval)
	while iterDate < endDate:
		result = db.get_values(tableName, iterDate, iterDate + increment)
		count = (len(result), 1)[len(result) == 0]
		data = round(reduce(lambda a, b: a + b[0], result, 0) / count, 2)

		graph['data'].append(data)
		graph['labels'].append(iterDate.strftime('%H:%M:%S'))

		iterDate += increment

	return graph