from core import db
from datetime import datetime

class RecentlyViewedArticle(db.Model):
    __tablename__ = 'recently_viewed_articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<RecentlyViewedArticle UserID: {self.user_id}, ArticleID: {self.article_id}, ViewedAt: {self.viewed_at}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def record_view(cls, user_id, article_id):
        # Check if the article was recently viewed by the user
        recent_view = cls.query.filter_by(user_id=user_id, article_id=article_id).first()
        if recent_view:
            recent_view.viewed_at = datetime.utcnow()  # Update timestamp
        else:
            recent_view = cls(user_id=user_id, article_id=article_id)
        recent_view.save()

    @classmethod
    def get_recently_viewed(cls, user_id, limit=5):
        return cls.query.filter_by(user_id=user_id).order_by(cls.viewed_at.desc()).limit(limit).all() 
