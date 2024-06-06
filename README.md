# FastAPI Web Application

This is a web application built with FastAPI following the MVC design pattern. The application interfaces with a MySQL database using SQLAlchemy for ORM and Pydantic for data validation. It includes features like user signup, login, and CRUD operations for posts with token-based authentication.

## Features

- User Signup
- User Login with JWT authentication
- Create, Read, and Delete posts
- In-memory caching for post retrieval
- Extensive field validation using Pydantic
- Dependency injection for database session and authentication

## Endpoints

### User Endpoints

- **Signup:** `POST /signup`
  - Request: `{ "email": "user@example.com", "password": "password" }`
  - Response: `{ "id": 1, "email": "user@example.com" }`

- **Login:** `POST /token`
  - Request: `{ "username": "user@example.com", "password": "password" }`
  - Response: `{ "access_token": "token", "token_type": "bearer" }`

### Post Endpoints

- **AddPost:** `POST /posts`
  - Request: `{ "text": "This is a new post" }` with Authorization header
  - Response: `{ "id": 1, "text": "This is a new post", "owner_id": 1 }`

- **GetPosts:** `GET /posts`
  - Response: `[ { "id": 1, "text": "This is a new post", "owner_id": 1 } ]`

- **DeletePost:** `DELETE /posts/{post_id}`
  - Response: `{ "id": 1, "text": "This is a new post", "owner_id": 1 }`

## API Documentation

This application includes automatically generated API documentation:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)


## Installation

### Prerequisites

- Python 3.8+
- MySQL database

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/fastapi-app.git
    cd fastapi-app
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the root directory with the following content:
      ```env
      DATABASE_URL=mysql+pymysql://username:password@localhost/dbname
      SECRET_KEY=your_secret_key
      ALGORITHM=HS256
      ACCESS_TOKEN_EXPIRE_MINUTES=30
      ```

5. Initialize the database:
    ```bash
    alembic upgrade head
    ```

6. Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```

## Project Structure

    ```bash
fastapi_app/
├── app/
│ ├── init.py
│ ├── main.py
│ ├── models.py
│ ├── schemas.py
│ ├── crud.py
│ ├── auth.py
│ ├── cache.py
│ ├── dependencies.py
│ └── routers/
│ ├── init.py
│ ├── auth.py
│ └── posts.py
├── migrations/
│ └── ... (Alembic migration files)
├── .env
├── requirements.txt
└── README.md
    ```


