from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    orders = db.relationship('Order', back_populates='user')

    @property
    def password(self):
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        return check_password_hash(self.password_hash,password)


orders_meals_association = db.Table('orders_meals',
                                    db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
                                    db.Column('meal_id', db.Integer, db.ForeignKey('meals.id'))
)


class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Integer)
    description = db.Column(db.String(200), nullable=False, unique=True)
    picture = db.Column(db.String(200))
    category = db.relationship("Category", back_populates='meals')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    orders = db.relationship('Order', secondary=orders_meals_association, back_populates='meals')


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    meals = db.relationship("Meal", back_populates='category')


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    status = db.Column(db.String(10))
    mail = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(50))
    meals = db.relationship('Meal', secondary=orders_meals_association, back_populates='orders')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='orders')

    @property
    def sum(self):
        return sum(m.price for m in self.meals)