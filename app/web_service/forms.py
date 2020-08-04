from flask_wtf import FlaskForm
from wtforms import Form, IntegerField, DateField, TimeField, validators, SelectField, FloatField
import shared_module.database as database

class LimitForm(FlaskForm):
	hiTemp = FloatField('hi_temperature')
	loTemp = FloatField('lo_temperature')
	hiSpeed = FloatField('hi_speed', validators=(validators.Optional(),))
	loSpeed = FloatField('lo_speed', validators=(validators.Optional(),))
	delay = FloatField('delay')

	def validate(self):
		if not Form.validate(self):
			return False
		return self.delay.data >= 0 and self.loTemp.data < self.hiTemp.data 
		#	and self.loSpeed.data < self.hiSpeed.data

class GraphForm(FlaskForm):
	beginDate = DateField('begin_date')
	beginTime = TimeField('begin_time')
	endDate = DateField('end_date')
	endTime = TimeField('end_time')
	sensorList = SelectField('sensorList', validate_choice=False)
	intervalList = SelectField('intervalList', validate_choice=False)

	def update_choices(self):
		db = database.SQLITE()
		names = {
			"reactive1_volume":"Volumen Tanque 1",
			"reactive2_volume":"Volumen Tanque 2",
			"reactive1_temperature":"Temperatura Reactivo 1",
			"reactive2_temperature":"Temperatura Reactivo 2",
			"reactor_temperature":"Temperatura en el Reactor",
			"reactive2_flow":"Caudal Reactivo 2",
			"reactive1_flow":"Caudal Reactivo 1",
			"agitator_speed": "Velocidad Agitador",
			"adc": "adc"
		}
		self.sensorList.choices = [(x, names[x]) for x in db.get_table_name() if not 'speed' in x and not 'flow' in x]
		self.intervalList.choices = [(1,"1seg"),(10,"10seg"),(15,"15seg"),(60,"1min"),(600,"10min"),(900,"15min"),(1800,"30min"),(3600,"1h"),(10800,"3h"),(43200,"12h")]

