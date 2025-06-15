from core import app
from core import db
from core.apis.article import article_resource
from core.apis.auth_routes import auth_resource

app.config['SECRET_KEY'] = 'your_secret_key' # Replace with a strong secret key

app.register_blueprint(article_resource, url_prefix = "/article")
app.register_blueprint(auth_resource, url_prefix = "/auth")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
