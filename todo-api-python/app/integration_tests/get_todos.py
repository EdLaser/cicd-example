import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app, get_db
from app.sql_app import models, schemas
from app.sql_app.database import engine


@pytest.fixture
def client():
    models.Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        yield client


def test_get_todos_empty(client, db: Session):
    # Test getting an empty list of todos
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == []


def test_get_todos_with_todos(client, db: Session):
    # Test getting a list of todos
    todos = [
        ToDo(title="Test Todo 1", description="Test Description 1"),
        ToDo(title="Test Todo 2", description="Test Description 2"),
        ToDo(title="Test Todo 3", description="Test Description 3"),
    ]
    db.add_all(todos)
    db.commit()

    response = client.get("/api")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["title"] == "Test Todo 1"
    assert response.json()[1]["title"] == "Test Todo 2"
    assert response.json()[2]["title"] == "Test Todo 3"


def test_get_todos_with_pagination(client, db: Session):
    # Test getting todos with pagination
    todos = [
        ToDo(title="Test Todo 1", description="Test Description 1"),
        ToDo(title="Test Todo 2", description="Test Description 2"),
        ToDo(title="Test Todo 3", description="Test Description 3"),
    ]
    db.add_all(todos)
    db.commit()

    response = client.get("/api?skip=1&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["title"] == "Test Todo 2"
    assert response.json()[1]["title"] == "Test Todo 3"
