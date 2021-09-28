from flask_wtf import FlaskForm
from .edit_game import MultiCheckboxField
from wtforms import SubmitField, StringField, validators, SelectField,\
    SelectMultipleField, MultipleFileField, DateField, FloatField, TextAreaField, widgets
from wtforms.widgets import FileInput
from wtforms.fields import FileField


class EditPublisher(FlaskForm):
    name = StringField('Имя издателя', [validators.DataRequired()])
    avatar_url = FileField('Фотография издателя', default='/static/missing_avatar.png')
    description = TextAreaField('Описание')
    submit = SubmitField('Подтвердить')