import os

current_path = os.path.dirname(os.path.realpath(__file__))


class Config:
    DEBUG = True
    SECRET_KEY = "randomstring"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USERNAME = "a@a.a"
    PASSWORD = "a@a.a"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    print('oh year')
