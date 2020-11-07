from datetime import date

import flask_migrate
from flask import Flask, render_template, session, redirect, request, url_for, flash, Markup
from flask_wtf.csrf import CSRFProtect

from config import Config
from models import db, User, Category, Meal, Order
from forms import LoginForm, RegisterForm, OrderForm

print('app has been run')


def create_app():
    res = Flask(__name__)
    res.config.from_object(Config)
    db.init_app(res)
    return res


app = create_app()
csrf = CSRFProtect()
csrf.init_app(app)
migrate = flask_migrate.Migrate(app, db)


@app.route('/')
@app.route('/index/')
def render_main():
    categories = db.session.query(Category).all()
    meals = db.session.query(Meal).filter(Meal.category_id == 1).limit(3).all()
    food = {}
    for c in categories:
        food[c.title] = db.session.query(Meal).filter(Meal.category_id == c.id).limit(3).all()
    return render_template("main.html", authorized=session.get('user_id'), categories=categories, meals=meals, food=food, cart=session.get("cart", {}))


@app.route('/cart/', methods=["GET", "POST"])
def cart():
    user = User()
    if session.get('user_id'):
        user = User.query.filter_by(id=int(session.get('user_id'))).first()
    else:
        flash(Markup("Чтобы сделать заказ – <a href='/login/'>войдите</a> или <a "
                     "href='/register/'>зарегистрируйтесь</a>"), 'warning')
    form = OrderForm()
    if form.validate_on_submit():
        ids = list(map(int,session.get('cart', {}).keys()))
        meals = db.session.query(Meal).filter(Meal.id.in_(ids)).all()
        order = Order(date=date.today(), mail=form.email.data, user_id=user.id)
        for meal in meals:
            order.meals.append(meal)
        db.session.add(order)
        db.session.commit()
        flash("Заказ был успешно сделан!", 'success')
        session.pop('cart')
        return render_template("ordered.html")
    if form.errors:
        flash("{}".format(form.errors), 'danger')
    return render_template("cart.html", form=form, cart=session.get("cart", {}), user=user)


@app.route('/addtocart/<m_id>/<title>/<int:price>/')
def render_add_to_cart(m_id, title, price):
    cart = session.get("cart", {})
    cart[m_id] = {"title": title, "price": price}
    session["cart"] = cart
    flash("Блюдо {} успешно добавлено в корзину!".format(title), 'success')
    return redirect(url_for("cart"))


@app.route('/deletefromcart/<m_id>/')
def render_delete_from_cart(m_id):
    cart = session.get("cart", {})
    if cart.get(m_id):
        cart.pop(m_id)
        flash("Блюдо было удалено из корзины", 'success')
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route('/account/')
def render_account():
    uid = session.get('user_id')
    if not uid:
        return redirect('/login/')
    user = User.query.filter_by(id=uid).first()
    print(user.name)
    return render_template("account.html", cart=session.get('cart', {}), orders=user.orders)


@app.route('/register/', methods=["GET", "POST"])
def render_register():
    error_msg = ""
    form = RegisterForm()
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if not username or not password or not email:
            error_msg = "Не все поля заполнены"
            return render_template("register.html", form=form, error_msg=error_msg)
        user = User(name=username, email=email)
        user.password = password
        db.session.add(user)
        db.session.commit()
        return f"{user.name}: Успешная регистрация"
    return render_template("register.html", form=form, error_mst=error_msg)


@app.route('/login/', methods=["GET", "POST"])
def render_login():
    form = LoginForm()
    if session.get("user_id"):
        return redirect(url_for('render_main', cart=session.get("cart", {})))
    error_msg = ""
    if request.method == "POST":
        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        user = User.query.filter(User.email == email).first()
        if user and user.password_valid(password):
            session['user_id'] = user.id
            session['is_auth'] = True
            return redirect(url_for('render_main', cart=session.get("cart", {})))
        else:
            error_msg += "Неверное имя или пароль"
            return error_msg

    return render_template("login.html", cart=session.get("cart"), form=form)


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
    if session.get("cart"):
        session.pop("cart")
    return "Cart is empty!"


if __name__ == '__main__':
    app.run()
