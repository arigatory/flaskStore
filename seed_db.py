from models import Category, Meal
import csv
from app import create_app, db
import config
import os

app = create_app()
app.app_context().push()


def seed_category():
    with open('categories.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = Category(id=int(row['id']), title=row['title'])
            db.session.add(category)
        db.session.commit()


def seed_meals():
    with open('meals.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            meal = Meal(id=int(row['id']),
                        title=row['title'],
                        price=int(row['price']),
                        description=row['description'],
                        picture=row['picture'],
                        category_id=int(row['category_id']))
            db.session.add(meal)
        db.session.commit()
