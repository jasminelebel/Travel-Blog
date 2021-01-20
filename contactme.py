from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class ContactMeForm(FlaskForm):
    body = StringField('Body')
    email = StringField('Email')
    submit = SubmitField('Submit')