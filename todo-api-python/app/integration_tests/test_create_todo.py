import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
import sql_app.models as models
from sqlalchemy.orm import sessionmaker, Session
from app.main import app
from app.sql_app.models import Base
from app.sql_app.database import engine


# Custom dependency to override get_db
def override_get_db():
    """Override the database session for dependency injection in FastAPI."""
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session_local()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture(scope="function")
def client():
    """Create a test client with overridden database dependencies."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    # Override the dependency
    app.dependency_overrides[app.get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Clear overrides after the test
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def db_session():
    """Fixture to provide a database session with transaction rollback for isolation."""
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_local()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


def test_create_todo(client: TestClient, db_session: Session):
    todo_data = {"title": "Test Todo", "description": "This is a test todo"}
    response = client.post("/api/new_todo", json=todo_data)
    assert response.status_code == 201
    created_todo = response.json()
    assert created_todo["title"] == "Test Todo"
    assert created_todo["description"] == "This is a test todo"
    assert not created_todo["is_done"]

    # Fetch from DB using the provided session
    db_todo = (
        db_session.query(models.ToDo)
        .filter(models.ToDo.id == created_todo["id"])
        .first()
    )
    assert db_todo is not None
    assert db_todo.title == "Test Todo"
    assert db_todo.description == "This is a test todo"
    assert not db_todo.is_done


def test_create_todo_missing_title(client: TestClient, db_session: Session):
    todo_data = {"description": "This is a test todo"}
    response = client.post("/api/new_todo", json=todo_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "title"]
    assert response.json()["detail"][0]["msg"] == "field required"


def test_create_todo_missing_description(client: TestClient, db_session: Session):
    todo_data = {"title": "Test Todo"}
    response = client.post("/api/new_todo", json=todo_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "description"]
    assert response.json()["detail"][0]["msg"] == "field required"
