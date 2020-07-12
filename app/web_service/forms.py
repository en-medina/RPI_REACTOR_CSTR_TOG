from flask_wtf import FlaskForm
from wtforms import Form, IntegerField, DateField, TimeField, validators, SelectField
import shared_module.database as database

class LimitForm(FlaskForm):
	hiTemp = IntegerField('hi_temperature')
	loTemp = IntegerField('lo_temperature')
	hiSpeed = IntegerField('hi_speed')
	loSpeed = IntegerField('lo_speed')

	def validate(self):
		if not Form.validate(self):
			return False
		return (self.loTemp.data < self.hiTemp.data and 
			self.loSpeed.data < self.hiSpeed.data)

class GraphForm(FlaskForm):
	beginDate = DateField('begin_date')
	beginTime = TimeField('begin_time')
	endDate = DateField('end_date')
	endTime = TimeField('end_time')
	sensorList = SelectField('sensorList', validate_choice=False)
	intervalList = SelectField('intervalList', validate_choice=False)

	def update_choices(self):
		db = database.SQLITE()
		self.sensorList.choices = [(x, x.replace('_',' ')) for x in db.get_table_name()]
		self.intervalList.choices = [(60,"1min"),(900,"15min"),(1800,"30min"),(3600,"1h"),(10800,"3h"),(43200,"12h")]

