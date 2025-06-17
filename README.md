# Content Management System

Design and implement a backend service that allows users to create, view, update, delete, and
list articles.
The service should also track and expose the "recently viewed" articles per user.

### Requirements
1. All functionality must be exposed over RESTful APIs ✅
2. Data must be persistent in a database. ✅
3. Build the ‘recently viewed’ feature using only basic collections and primitives. Avoid any third-party or built-in utilities✅
4. Provide a Dockerfile to containerize the service and docker-compose.yml to run the full stack (separate DB container) ✅
5. Include a README.md that explains how to build and run the service (locally and via Docker). ✅

### Bonus Points
1. Authentication: Add simple token-based auth so each user only sees their own to-dos ✅
2. Implement pagination for list articles API ✅
3. Database schema changelog management ✅
4. Unit tests

## Technologies Used

*   **Flask**: Python backend framework
*   **PostgreSQL**: Database for application.
*   **SQLAlchemy**: ORM for database interaction and management.
*   **Marshmallow**: For serialization/deserialization and validation of data.
*   **PyJWT**: For token based authentication.
*   **Flask-Migrate**: For Database schema changelog management 
*   **Docker**: Containerization

## Instructions to run with Docker

1. Make sure to have Docker installed.
2. Navigate to the root directory of the project.
3. Run `docker-compose up --build` to build and start the services.
4. The backend application will be accessible at `http://localhost:5000`.
5. Press `Ctrl + C` to stop the application.
6. Run `docker-compose down` to remove the containers, networks, and volumes.  


## Instructions to to run locally

1. Make sure to have Python (3.7+) and `pip` installed.
2. Navigate to the root directory of the project.
3. Create a virtual environment: `python -m venv env`.
4. Activate the virtual environment using `.\env\Scripts\activate` (Windows) OR `source env/bin/activate` (Linux)
5. Set environment variables for SECRET_KEY, POSTGRES_USERNAME and POSTGRES_PASSWORD:
   - Windows: `set SECRET_KEY=<secret_key>`  
   `set POSTGRES_USERNAME=<username> `  
   `set POSTGRES_PASSWORD=<password>`
   - Linux: `export SECRET_KEY=<secret_key>`  
   `export POSTGRES_USERNAME=<username>`   
   `export POSTGRES_PASSWORD=<password>`
5. Install the dependencies: `pip install -r requirements.txt`.
7. Run the application: `python core/server.py`.
8. The web application will be accessible at `http://localhost:5000`.
9. Press `Ctrl + C` to stop the application.

## API Endpoints

### Authentication Endpoints

-   `POST /auth/login`: User login, returns JWT token.
    -   **Request Body:** `{"username": "your_username", "password": "your_password"}`
    -   **Response:** `{"token": "your_jwt_token"}`

-   `POST /auth/register`: User registration, returns JWT token.
    -   **Request Body:** `{"username": "new_username", "password": "new_password"}`
    -   **Response:** `{"token": "your_jwt_token"}`

### Article API Endpoints (All requires Authentication Token in Header `Authorization: Bearer <token>` )

-   `GET /article/`: Get all articles for the user.
    -   **Response:** `[{"id": 1, "title": "Article 1", "content": "Content 1", "author_id": 1}, ...]`

-   `GET /article/<int:article_id>`: Get a specific article by ID for the user.
    -   **Response:** `{"id": 1, "title": "Article 1", "content": "Content 1", "author_id": 1}`

-   `POST /article/`: Create a new article.
    -   **Request Body:** `{"title": "New Article Title", "content": "New Article Content"}`
    -   **Response:** `{"id": 2, "title": "New Article Title", "content": "New Article Content", "author_id": 1}`

-   `PUT /article/`: Update an existing article.
    -   **Request Body:** `{"id": 1, "title": "Updated Title", "content": "Updated Content"}`
    -   **Response:** `{"id": 1, "title": "Updated Title", "content": "Updated Content", "author_id": 1}`

-   `DELETE /article/`: Delete an article.
    -   **Request Body:** `{"id": 1}`
    -   **Response:** `{"message": "Article deleted successfully"}`

-   `GET /article/recently-viewed`: Get recently viewed articles for the user.
    -   **Response:** `[{"id": 1, "article_id": 1, "viewed_at": "timestamp", "user_id": 1}, ...]`

-   `GET /article/paginated`: Get all articles with pagination for the user.
    -   **Query Parameters:** `page` (optional, default: 1), `page_size` (optional, default: 10)
    -   **Response:** `{"articles": [{"id": 1, "title": "Article 1", "content": "Content 1", "author_id": 1}, ...], "total_pages": 5, "current_page": 1, "total_articles": 50, "has_next": true}`
