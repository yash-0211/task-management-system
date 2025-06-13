import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    print(SECRET_KEY)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///task_management.sqlite3'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = Config()
