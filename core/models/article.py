from core import db
from http import HTTPStatus

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, unique= True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Article {self.title}>"
    
    @classmethod
    def get_articles_by_author(cls, author_id):
        return cls.query.filter(cls.author_id == author_id).all()
    
    @classmethod
    def get(cls, article_id, author_id):
        article = cls.query.filter(cls.author_id == author_id, cls.id == article_id).first()
        if not article:
            raise Exception("Article not found", HTTPStatus.NOT_FOUND)
        return article

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls, article_id, user_id):
        article = cls.get(article_id=article_id, author_id=user_id)
        if not article:
            raise Exception("Article not found", HTTPStatus.NOT_FOUND)
        
        db.session.delete(article)
        db.session.commit()

    def edit(self, payload, author_id):
        
        # Check for title conflict with other articles by the same author
        title = payload.title
        existing_article = Article.query.filter(
            Article.title == title,
            Article.author_id == author_id,
            Article.id != self.id
        ).first()

        if existing_article:
            raise Exception("Conflict: An article with this title already exists.", HTTPStatus.CONFLICT)

        self.title = payload.title
        self.content = payload.content
        db.session.commit()
        return self
