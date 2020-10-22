from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def render_main():
    return render_template("main.html")


@app.route('/cart/')
def render_cart():
    return render_template("cart.html")


@app.route('/account/')
def render_account():
    return render_template("account.html")


@app.route('/login/')
def render_login():
    return render_template("login.html")


@app.route('/logout/')
def render_logout():
    return render_template("auth.html")


if __name__ == '__main__':
    app.run()
