from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, SubmitField
from wtforms.validators import DataRequired

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time')
    submit = SubmitField('Add Event')
