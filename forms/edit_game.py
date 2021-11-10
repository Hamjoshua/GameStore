from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, validators, SelectField,\
    SelectMultipleField, DateField, FloatField, TextAreaField, widgets, IntegerField


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class EditGame(FlaskForm):
    name = StringField('Название', [validators.DataRequired()])
    genres = MultiCheckboxField('Жанры', [validators.DataRequired()], coerce=int)
    platforms = MultiCheckboxField('Платформы', [validators.DataRequired()], coerce=int)
    developer = SelectField('Разработчик', [validators.DataRequired()])
    publisher = SelectField('Издатель', [validators.DataRequired()])
    release_date = DateField('Дата релиза')
    rating = FloatField('Рейтинг', [validators.NumberRange(min=0, max=10)])
    description = TextAreaField('Описание')
    price = IntegerField('Стоимость', [validators.NumberRange(min=0)])
    submit = SubmitField('Подтвердить')
