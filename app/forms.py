from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    username = StringField('用户名：', validators=[DataRequired()])
    authkey = StringField('注册口令：', validators=[DataRequired()])
    pwd = PasswordField('密 码：', validators=[DataRequired(), Length(min=8, max=20)])
    confirm = PasswordField('确认密码：', validators=[DataRequired(), EqualTo('pwd')])
    submit = SubmitField('提 交')

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if user and user.registered:
            raise ValidationError("user already exsist")

class ResetForm(FlaskForm):
    username = StringField('用户名：', validators=[DataRequired()])
    authkey = StringField('注册口令：', validators=[DataRequired()])
    pwd = PasswordField('密 码：', validators=[DataRequired(), Length(min=8, max=20)])
    confirm = PasswordField('确认密码：', validators=[DataRequired(), EqualTo('pwd')])
    submit = SubmitField('提 交')

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if (not user) or (not user.registered):
            raise ValidationError("user not exsist")

class LoginForm(FlaskForm):
    username = StringField('用户名：', validators=[DataRequired()])
    password = PasswordField('密  码：', validators=[DataRequired()])
    submit = SubmitField('登  录')

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data)
        if not user:
            raise ValidationError('用户名不存在。')

class AppendForm(FlaskForm):
    username = StringField('用户名：', validators=[DataRequired()])
    submit = SubmitField('添 加')

    def already_exsist(self, name):
        user = User.query.filter_by(name=name).first()
        if user:
            return True
        else:
            return False
