from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Optional, InputRequired

class Signup(FlaskForm):
    """User can signup"""
    name = StringField('Name:', validators=[InputRequired()])
    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])