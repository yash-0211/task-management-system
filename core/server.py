from core import app, db
from api.article import article_resource

app.register_blueprint(article_resource, url_prefix = "/article")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
