from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email, InputRequired


class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль:", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField("Имя:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль:", validators=[DataRequired()])
    password_check = PasswordField("Повторите пароль:", validators=[DataRequired()])


class OrderForm(FlaskForm):
    name = StringField("Ваше имя")
    email = StringField("Email:", validators=[InputRequired(), Email()])
    phone = StringField("Телефон:", validators=[DataRequired("Требуется ввести телефон"), InputRequired()])
    address = StringField("Адрес")
    submit = SubmitField('Оформить заказ')