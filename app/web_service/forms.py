from flask_wtf import FlaskForm
from wtforms import Form, IntegerField, validators

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