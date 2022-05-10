from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    pokemon = StringField('Enter Pokemon Name', validators=[DataRequired()])
    submit = SubmitField('Submit')