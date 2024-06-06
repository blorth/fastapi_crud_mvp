from fastapi import FastAPI
from .routers import auth, posts
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Web Application",
    description="This is a web application built with FastAPI following the MVC design pattern. The application interfaces with a MySQL database using SQLAlchemy for ORM and Pydantic for data validation. It includes features like user signup, login, and CRUD operations for posts with token-based authentication.",
    version="1.0.0",
    openapi_tags=[
        {"name": "auth", "description": "Operations related to user authentication."},
        {"name": "posts", "description": "Operations related to posts."},
    ]
)

app.include_router(auth.router)
app.include_router(posts.router)
