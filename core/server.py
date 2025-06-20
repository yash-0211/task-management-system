from core import app
from core import db
from core.apis.article import article_resource
from core.apis.auth_routes import auth_resource
from core import models
from flask_migrate import Migrate

app.register_blueprint(article_resource, url_prefix = "/article")
app.register_blueprint(auth_resource, url_prefix = "/auth")

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
