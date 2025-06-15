from core import db

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
