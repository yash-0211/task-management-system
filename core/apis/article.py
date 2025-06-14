from flask import Blueprint, request
from core import db
from schema import ArticleSchema, ArticleCreateSchema, ArticleUpdateSchema, ArticleIdSchema
from core.models.article import Article
from core.models.user import User
from response import APIResponse

article_resource = Blueprint('article_resource', __name__)


@article_resource.route('/', methods=['GET'])
def get_all_articles(p):
    """ Get all articles """

    all_articles = Article.get_articles_by_author(author_id=p.id)
    article_dump = ArticleSchema().dump(all_articles, many=True)
    return APIResponse.respond(article_dump)


@article_resource.route('/<int:article_id>', methods=['GET'])
def get_article(p, article_id):
    """ Get an article by id """

    article = Article.get(article_id=article_id, author_id=p.id)
    article_dump = ArticleSchema().dump(article)
    return APIResponse.respond(article_dump)


@article_resource.route('/', methods=['POST'])
def create_article(p, incoming_payload):
    """ Create a new article """

    # Check if article title already exists
    article_title = incoming_payload.get('title')
    existing_article = Article.query.filter_by(title=article_title, author_id=p.id).first()
    if existing_article:
        return APIResponse.respond({'message': 'Article with this title already exists for this author'}, status_code=409)

    article = ArticleCreateSchema().load(incoming_payload)
    article.author_id = p.id
    article.save()
    article_dump = ArticleSchema().dump(article)
    return APIResponse.respond(article_dump)


@article_resource.route('/', methods=['PUT'])
def update_article(p, incoming_payload):
    """ Update an article """

    updated_article_obj = ArticleUpdateSchema(partial=True).load(incoming_payload)
    article = Article.get(article_id=updated_article_obj.id, author_id=p.id)

    article = article.edit(updated_article_obj, p.id)

    article_dump = ArticleSchema().dump(article)
    return APIResponse.respond(article_dump)


@article_resource.route('/', methods=['DELETE'])
def delete_article(p, incoming_payload):
    """ Delete an article """

    article_obj = ArticleIdSchema().load(incoming_payload)
    article_id = article_obj.id
    
    Article.delete(article_id=article_id, author_id=p.id)
    return APIResponse.respond({'message': 'Article deleted successfully'})
