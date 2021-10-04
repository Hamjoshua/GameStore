from flask_wtf import FlaskForm
from wtforms import validators
from .edit_game import MultiCheckboxField, StringField


class LiteSearch(FlaskForm):
    search_field = StringField('Поиск по имени')
    genres = MultiCheckboxField('Жанры', [validators.DataRequired()], coerce=int)
    platforms = MultiCheckboxField('Платформы', [validators.DataRequired()], coerce=int)