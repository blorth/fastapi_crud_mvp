import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User
from app.auth import create_access_token

# Create a test database URL
DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")

# Create a new SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a new sessionmaker
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create the test database tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    # Set up the database before running tests
    Base.metadata.create_all(bind=engine)
    yield
    # Tear down the database after tests
    Base.metadata.drop_all(bind=engine)

def test_signup(test_db):
    response = client.post("/signup", json={"email": "test@example.com", "password": "password"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_login(test_db):
    response = client.post("/token", data={"username": "test@example.com", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.fixture
def auth_token(test_db):
    response = client.post("/token", data={"username": "test@example.com", "password": "password"})
    return response.json()["access_token"]

def test_create_post(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/posts", json={"text": "This is a test post"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["text"] == "This is a test post"

def test_get_posts(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/posts", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_post(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/posts", json={"text": "Post to be deleted"}, headers=headers)
    post_id = response.json()["id"]
    delete_response = client.delete(f"/posts/{post_id}", headers=headers)
    assert delete_response.status_code == 200
    assert delete_response.json()["id"] == post_id
