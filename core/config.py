import os

DB_USERNAME = os.environ.get('POSTGRES_USERNAME')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

DB_HOST = "db"
DB_PORT = 5432
DB_NAME = "content_management"

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = Config()
