from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config
from core import models
from core.apis.article import article_api

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config)
app.app_context().push()

db = SQLAlchemy(app)

app.register_blueprint(article_api)

