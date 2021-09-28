from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, validators


class BuyGame(FlaskForm):
    code = StringField('Проверочный код', validators=[validators.DataRequired()])
    submit = SubmitField('Отправить')