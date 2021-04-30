from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])

class LoginForm(FlaskForm):
    name = StringField('姓名', validators=[InputRequired()])
    password = PasswordField('密码', validators=[InputRequired()])
