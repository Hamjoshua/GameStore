from flask_wtf import FlaskForm
from wtforms import validators
from .edit_game import MultiCheckboxField


class LiteSearch(FlaskForm):
    genres = MultiCheckboxField('Жанры', [validators.DataRequired()], coerce=int)
    platforms = MultiCheckboxField('Платформы', [validators.DataRequired()], coerce=int)