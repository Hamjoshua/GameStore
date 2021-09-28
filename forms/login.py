from wtforms import StringField, PasswordField, validators, SubmitField
from flask_wtf import FlaskForm


class Login(FlaskForm):
    email = StringField('Адрес почты', validators=[validators.DataRequired()])
    password = PasswordField('Пароль', validators=[validators.DataRequired()])
    submit = SubmitField('Войти')