import shared_module.database as database
from datetime import timedelta
from functools import reduce


def generate_graph(tableName, beginDate, endDate, interval=60):
	db = database.SQLITE()
	graph = {
		'title':tableName.replace('_',' '),
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
		graph['labels'].append(iterDate.strftime('%H:%M'))

		iterDate += increment

	return graph