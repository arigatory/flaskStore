from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email


class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль:", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField("Имя:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль:", validators=[DataRequired()])


class OrderForm(FlaskForm):
    name = StringField("Ваше имя")
    mail = StringField("Email:", validators=[DataRequired(), Email()])
    phone = StringField("Телефон:", validators=[DataRequired(), Length(min=9)])
    address = StringField("Адрес")
    submit = SubmitField('Оформить заказ')