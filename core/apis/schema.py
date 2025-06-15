from marshmallow import EXCLUDE, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.article import Article
from core.models.user import User
from core.models.recently_viewed_article import RecentlyViewedArticle


class ArticleIdSchema(SQLAlchemyAutoSchema):
    # Input Schema for operations requiring only article id
    class Meta:
        model = Article
        unknown = EXCLUDE
        load_instance = True

    id = auto_field(required=True, allow_none=False)

    @post_load
    def make_article(self, data_dict, many, partial):
        return Article(**data_dict)


class ArticleSchema(SQLAlchemyAutoSchema):
    # Output Schema
    class Meta:
        model = Article
        unknown = EXCLUDE
    
    id = auto_field(required=True)
    title = auto_field(required = True)
    content = auto_field(required = True)
    author_id = auto_field(dump_only = True)

    @post_load
    def initiate_class(self, data_dict, many, partial):
        return Article(**data_dict)


class ArticleCreateSchema(SQLAlchemyAutoSchema):
    # Input Schema for Create
    class Meta:
        model = Article
        unknown = EXCLUDE
        load_instance = True

    title = auto_field(required=True)
    content = auto_field(required=True)

    @post_load
    def make_article(self, data_dict, many, partial):
        return Article(**data_dict)


class ArticleUpdateSchema(SQLAlchemyAutoSchema):
    # Input Schema for Update
    class Meta:
        model = Article
        unknown = EXCLUDE
        load_instance = True

    id = auto_field(required=True, allow_none=False)
    title = auto_field(required=False)
    content = auto_field(required=False)

    @post_load
    def make_article(self, data_dict, many, partial):
        return Article(**data_dict)


class RecentlyViewedArticleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RecentlyViewedArticle
        unknown = EXCLUDE
        load_instance = True
    
    id = auto_field(required=True)
    user_id = auto_field(required=True)
    article_id = auto_field(required=True)
    viewed_at = auto_field(required=True)

    @post_load
    def make_recently_viewed_article(self, data_dict, many, partial):
        return RecentlyViewedArticle(**data_dict)

