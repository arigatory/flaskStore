from flask_migrate import Migrate
from flask import Flask, render_template, session, redirect, request, url_for
from config import Config
from models import db, User, Category, Meal
from forms import LoginForm, RegisterForm, OrderForm

print('app has been run')


def create_app():
    res = Flask(__name__)
    res.config.from_object(Config)
    db.init_app(res)
    return res


app = create_app()
migrate = Migrate(app, db)


@app.route('/')
@app.route('/index/')
def render_main():
    if not session.get('user_id'):
        print('not is user_id!')
        return redirect('/login/')
    categories = db.session.query(Category).all()
    meals = db.session.query(Meal).filter(Meal.category_id == 1).limit(3).all()
    food = {}
    for c in categories:
        food[c.title] = db.session.query(Meal).filter(Meal.category_id == c.id).limit(3).all()
    return render_template("main.html", categories=categories, meals=meals, food=food, cart=session.get("cart", {}))


@app.route('/cart/', methods=["GET", "POST"])
def render_cart():
    form = OrderForm()
    if request.method == "POST":
        if form.validate_on_submit():
            return render_template("ordered.html")
        redirect(url_for("reset_cart"))
    return render_template("cart.html", form=form, cart=session.get("cart", {}))


@app.route('/addtocart/<m_id>/<title>/<int:price>/')
def render_add_to_cart(m_id, title, price):
    cart = session.get("cart", {})
    cart[m_id] = {"title": title, "price": price}
    session["cart"] = cart
    return redirect(url_for("render_cart"))


@app.route('/deletefromcart/<m_id>/')
def render_delete_from_cart(m_id):
    cart = session.get("cart", {})
    if cart.get(m_id):
        cart.pop(m_id)
    session["cart"] = cart
    return redirect(url_for("render_cart", deleted=True))


@app.route('/account/')
def render_account():
    return render_template("account.html")


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
        user = User(name=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return f"{user.name}: Успешная регистрация"
    return render_template("register.html", form=form, error_mst=error_msg)


@app.route('/login/', methods=["GET", "POST"])
def render_login():
    if session.get("user_id"):
        return redirect(url_for('render_main', cart=session.get("cart", {})))
    error_msg = ""
    if request.method == "POST":
        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        user = User.query.filter(User.email == email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['is_auth'] = True
            return redirect(url_for('render_main', cart=session.get("cart", {})))
        else:
            error_msg += "Неверное имя или пароль"
            return error_msg

    return render_template("login.html", cart=session.get("cart"))


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
    if session.get("cart"):
        session.pop("cart")
    return "Cart is empty!"


@app.route('/dark/')
def dark_on():
    session['dark'] = True
    return '<body bgcolor={}><a href="/">INDEX</a><a href="/dark">Темную вкл</a><br><a href="/white">Темную ' \
           'выкл</a></body>'.format('#000' if session['dark'] else '#fff')


@app.route('/white/')
def dark_off():
    session['dark'] = False
    return '<body bgcolor={}><a href="/">INDEX</a><a href="/dark">Темную вкл</a><br><a href="/white">Темную ' \
           'выкл</a></body>'.format('#000' if session['dark'] else '#fff')


@app.route('/auth/')
def auth():
    return render_template('auth.html')


if __name__ == '__main__':
    app.run()
