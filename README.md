# Content Management System

Design and implement a backend service that allows users to create, view, update, delete, and
list articles.
The service should also track and expose the “recently viewed” articles per user.
## How to run with Docker

1. Make sure you have Docker installed.
2. Navigate to the root directory of the project in your terminal.
3. Run `docker-compose up --build` to build and start the services.
4. The web application will be accessible at `http://localhost:5000`.

## How to run locally

1. Make sure you have Python (3.7+) and `pip` installed.
2. Navigate to the root directory of the project in your terminal.
3. Create a virtual environment: `python -m venv env`.
4. Activate the virtual environment:
    - On Windows: `.\env\Scripts\activate`
    - On macOS/Linux: `source env/bin/activate`
5. Install the required dependencies: `pip install -r requirements.txt`.
6. Navigate to the `core` directory: `cd core`.
7. Run the application: `python server.py`.
8. The web application will be accessible at `http://localhost:5000`.

## API Endpoints

### Authentication Endpoints

-   `POST /auth/login`: User login, returns JWT token.
    -   **Request Body:** `{"username": "your_username", "password": "your_password"}`
    -   **Response:** `{"token": "your_jwt_token"}`

-   `POST /auth/register`: User registration, returns JWT token.
    -   **Request Body:** `{"username": "new_username", "password": "new_password"}`
    -   **Response:** `{"token": "your_jwt_token"}`

### Article API Endpoints (Requires Authentication Token in Header `Authorization: Bearer <token>` )

-   `GET /article/`: Get all articles for the authenticated user.
    -   **Response:** `[{"id": 1, "title": "Article 1", "content": "Content 1", "author_id": 1}, ...]`

-   `GET /article/<int:article_id>`: Get a specific article by ID for the authenticated user.
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

-   `GET /article/recently-viewed`: Get recently viewed articles for the authenticated user.
    -   **Response:** `[{"id": 1, "article_id": 1, "viewed_at": "timestamp", "user_id": 1}, ...]`
