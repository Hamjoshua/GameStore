from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, StringField, SubmitField, DateField


class EditUser(FlaskForm):
    name = StringField('Настоящее имя')
    description = TextAreaField('О себе')

    address = StringField('Адрес проживания')
    birthday = DateField('День рождения')
    avatar_url = FileField('Фото профиля')
    bg_url = FileField('Едж-фон профиля')
    body_bg_url = FileField('Фон профиля')
    submit = SubmitField('Изменить')
