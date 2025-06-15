from flask import Blueprint, request
from core import db
from .schema import ArticleSchema, ArticleCreateSchema, ArticleUpdateSchema, ArticleIdSchema, RecentlyViewedArticleSchema
from core.models.article import Article
from core.models.user import User
from core.models.recently_viewed_article import RecentlyViewedArticle
from .response import APIResponse
from .auth import token_required

RECENTLY_VIEWED_ARTICLES_LIMIT = 10

article_resource = Blueprint('article_resource', __name__)


@article_resource.route('/', methods=['GET'])
@token_required
def get_all_articles(**kwargs):
    """ Get all articles """
    user_id = kwargs['user_id'].id
    user = User.get_user(id=user_id)
    all_articles = user.articles
    article_dump = ArticleSchema().dump(all_articles, many=True)
    return APIResponse.respond(article_dump)


@article_resource.route('/<int:article_id>', methods=['GET'])
@token_required
def get_article(article_id, **kwargs):
    """ Get an article by id """
    user_id = kwargs['user_id'].id
    user = User.get_user(id=user_id)
    article = user.articles.filter_by(id=article_id).first()
    if not article:
        return APIResponse.respond({'message': 'Article not found'}, status_code=404)
    
    RecentlyViewedArticle.record_view(user_id=user_id, article_id=article.id)
    article_dump = ArticleSchema().dump(article)
    return APIResponse.respond(article_dump)


@article_resource.route('/', methods=['POST'])
@token_required
def create_article(incoming_payload, **kwargs):
    """ Create a new article """
    user_id = kwargs['user_id'].id
    # Check if article title already exists
    article_title = incoming_payload.get('title')
    existing_article = Article.query.filter_by(title=article_title, author_id=user_id).first()
    if existing_article:
        return APIResponse.respond({'message': 'Article with this title already exists for this author'}, status_code=409)

    article = ArticleCreateSchema().load(incoming_payload)
    article.author_id = user_id
    article.save()
    RecentlyViewedArticle.record_view(user_id= user_id, article_id=article.id)
    article_dump = ArticleSchema().dump(article)
    return APIResponse.respond(article_dump)


@article_resource.route('/', methods=['PUT'])
@token_required
def update_article(incoming_payload, **kwargs):
    """ Update an article """
    user_id = kwargs['user_id'].id
    updated_article_obj = ArticleUpdateSchema(partial=True).load(incoming_payload)
    article = Article.get(article_id=updated_article_obj.id, author_id=user_id)

    article = article.edit(updated_article_obj, user_id)
    RecentlyViewedArticle.record_view(user_id=user_id, article_id=article.id)
    article_dump = ArticleSchema().dump(article)
    return APIResponse.respond(article_dump)


@article_resource.route('/', methods=['DELETE'])
@token_required
def delete_article(incoming_payload, **kwargs):
    """ Delete an article """
    user_id = kwargs['user_id'].id
    article_obj = ArticleIdSchema().load(incoming_payload)
    article_id = article_obj.id
    
    Article.delete(article_id=article_id, author_id=user_id)
    return APIResponse.respond({'message': 'Article deleted successfully'})


@article_resource.route('/recently-viewed', methods=['GET'])
@token_required
def get_recently_viewed_articles(**kwargs):
    """ Get recently viewed articles by user """
    user_id = kwargs['user_id'].id
    recently_viewed = RecentlyViewedArticle.get_recently_viewed(user_id=user_id, limit=RECENTLY_VIEWED_ARTICLES_LIMIT)
    if not recently_viewed:
        return APIResponse.respond({'message': 'No recently viewed articles'}, status_code=200)
    
    recently_viewed_dump = RecentlyViewedArticleSchema(many=True).dump(recently_viewed)
    return APIResponse.respond(recently_viewed_dump)
