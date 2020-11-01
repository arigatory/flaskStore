from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import csv

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), nullable=False)


class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Integer)
    description = db.Column(db.String(200), nullable=False, unique=True)
    picture = db.Column(db.String(200))
    category = db.relationship("Category", back_populates='meals')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    meals = db.relationship("Meal", back_populates='category')


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    sum = db.Column(db.Integer)
    status = db.Column(db.String(10))
    mail = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(50))
    meals = db.Column(db.String())



