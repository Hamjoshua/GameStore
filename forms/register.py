from wtforms import StringField, DateField, PasswordField,\
    validators, TextAreaField, SubmitField
from flask_wtf import FlaskForm


class Register(FlaskForm):
    login = StringField('Логин', validators=[validators.DataRequired()])
    name = StringField('Настоящее имя')
    password = PasswordField('Пароль',
                             validators=[validators.DataRequired(),
                                         validators.equal_to('confirm', 'Пароли должны совпадать')])
    confirm = PasswordField('Подтвердите пароль', validators=[validators.DataRequired()])
    email = StringField('Адрес почты', validators=[validators.DataRequired()])
    address = StringField('Адрес проживания')
    birthday = DateField('День рождения')
    description = TextAreaField('О себе')
    submit = SubmitField('Зарегистрироваться')
