import unittest
import json
from core import app, db
from core.models.article import Article
from core.models.user import User

class ArticleAPITestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_task_management.sqlite3'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            # Create a test user
            self.test_user_staff = User(username='teststaff', password='password')
            self.test_user_principal = User(username='testprincipal', password='password')
            db.session.add(self.test_user_staff)
            db.session.add(self.test_user_principal)
            db.session.commit()
            self.staff_user_id = self.test_user_staff.id
            self.principal_user_id = self.test_user_principal.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_article(self):
        with app.app_context():
            response = self.app.post('/articles', data=json.dumps({
                'title': 'Test Article',
                'content': 'This is a test article.',
                'author_id': self.staff_user_id
            }), content_type='application/json')
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertEqual(data['message'], 'Article created successfully')
            self.assertEqual(data['data']['title'], 'Test Article')

    def test_get_articles(self):
        with app.app_context():
            article1 = Article(title='Article 1', content='Content 1', author_id=self.staff_user_id)
            article2 = Article(title='Article 2', content='Content 2', author_id=self.principal_user_id)
            db.session.add(article1)
            db.session.add(article2)
            db.session.commit()

            response = self.app.get('/articles')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(len(data['data']), 2)

    def test_get_article_by_id(self):
        with app.app_context():
            article = Article(title='Single Article', content='Content for single article', author_id=self.staff_user_id)
            db.session.add(article)
            db.session.commit()

            response = self.app.get(f'/articles/{article.id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['data']['title'], 'Single Article')

    def test_update_article(self):
        with app.app_context():
            article = Article(title='Original Title', content='Original Content', author_id=self.staff_user_id)
            db.session.add(article)
            db.session.commit()

            response = self.app.put(f'/articles/{article.id}', data=json.dumps({
                'title': 'Updated Title',
                'content': 'Updated Content'
            }), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['message'], 'Article updated successfully')
            self.assertEqual(data['data']['title'], 'Updated Title')
            self.assertEqual(data['data']['content'], 'Updated Content')

    def test_delete_article(self):
        with app.app_context():
            article = Article(title='Article to Delete', content='Content to delete', author_id=self.principal_user_id)
            db.session.add(article)
            db.session.commit()

            response = self.app.delete(f'/articles/{article.id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['message'], 'Article deleted successfully')

            # Verify article is deleted
            response = self.app.get(f'/articles/{article.id}')
            self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main() 