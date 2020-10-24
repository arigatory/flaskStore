from app import db, User
user = User(username="ivan", password='test', email="ya@ya.ru")
db.session.add(user)
db.session.commit()