from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, session, redirect, request, url_for
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

app = Flask(__name__)
app.secret_key = "randomstring"
app.config['USERNAME'] = "a@a.a"
app.config['PASSWORD'] = "a@a.a"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class LoginForm(FlaskForm):
    username = StringField("Имя:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль:", validators=[DataRequired()])


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), nullable=False)


@app.route('/')
@app.route('/index/')
def render_main():
    if not session.get('user_id'):
        print('not is user_id!')
        return redirect('/login/')
    return render_template("main.html")


@app.route('/cart/')
def render_cart():
    return render_template("cart.html")


@app.route('/account/')
def render_account():
    return render_template("account.html")


@app.route('/register/', methods=["GET", "POST"])
def render_register():
    form = LoginForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("register.html", form=form)
        user = User.query.filter(User.name == form.username.data).first()
        if not user or user.password != form.password.data:
            form.username.errors.append("Неверное имя или пароль")
        else:
            session["user_id"] = user.id
            return redirect("/")
    return render_template("register.html",form=form)


@app.route('/login/', methods=["GET", "POST"])
def render_login():
    if session.get("user_id"):
        return render_template('main.html')
    error_msg = ""
    print('no redirect!')
    if request.method == "POST":
        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        user = User.query.filter(User.email == email).first()
        print('----------------->OK')
        if user and user.password == password:
            session['user_id'] = user.id
            session['is_auth'] = True
            return redirect("/")
        else:
            error_msg += "Неверное имя или пароль"
            return error_msg

    return render_template("login.html")


@app.route('/logout/')
def render_logout():
    if session.get("user_id"):
        session.pop("user_id")
    return redirect('/login/')


@app.route('/add/<item>/')
def add_to_cart(item):
    cart = session.get("cart", [])
    cart.append(item)
    session['cart'] = cart
    return f"Item {item} added"


@app.route('/reset/')
def reset_cart():
    # удаляем корзину из сессии
    session.pop("cart")
    return "Cart is empty!"


@app.route('/dark/')
def dark_on():
    session['dark'] = True
    return '<body bgcolor={}><a href="/">INDEX</a><a href="/dark">Темную вкл</a><br><a href="/white">Темную выкл</a></body>'.format(
        '#000' if session['dark'] else '#fff')


@app.route('/white/')
def dark_off():
    session['dark'] = False
    return '<body bgcolor={}><a href="/">INDEX</a><a href="/dark">Темную вкл</a><br><a href="/white">Темную выкл</a></body>'.format(
        '#000' if session['dark'] else '#fff')


@app.route('/auth/')
def auth():
    return render_template('auth.html')

if __name__ == '__main__':
    app.run()
