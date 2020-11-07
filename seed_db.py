from models import Category, Meal, Order, User
import csv
from app import create_app, db
from datetime import date, timedelta


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


def seed_users():
    user = User(name='test', email='t@t.t', id=1)
    user.password = '123'
    db.session.add(user)
    db.session.commit()


def seed_orders():
    order1 = Order(date=date.today(), status='Выполнен', user_id=1, address='Москва, ул. Центральная, д.46, кв. 77', phone='+79995554444')
    meals = Meal.query.filter(Meal.id <= 3).all()
    for m in meals:
        order1.meals.append(m)
    order2 = Order(date=(date.today()-timedelta(days=1)), status='Выполнен', user_id=1, address='Москва, ул. Центральная, д.46, кв. 77', phone='+79995554444')
    meal = Meal.query.filter(Meal.id == 4).first()
    order2.meals.append(meal)
    db.session.add(order1)
    db.session.add(order2)
    db.session.commit()


def clean_db():
    orders = db.session.query(Order).all()
    for order in orders:
        for m in order.meals:
            db.session.delete(m)
    db.session.query(Order).delete(synchronize_session=False)
    db.session.query(Meal).delete(synchronize_session=False)
    db.session.query(Category).delete(synchronize_session=False)
    db.session.query(User).delete(synchronize_session=False)
    db.session.commit()


def seed():
    clean_db()
    seed_users()
    seed_category()
    seed_meals()
    seed_orders()
