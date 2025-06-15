from core import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    articles = db.relationship('Article', backref='author', lazy=True)
    recently_viewed_articles = db.relationship('RecentlyViewedArticle', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
        
    @classmethod
    def get_user(cls, id):
        return cls.query.filter_by(id=id).first()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
