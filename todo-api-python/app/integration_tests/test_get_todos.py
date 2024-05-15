from os import environ
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.main import app
from app.sql_app.models import Base, ToDo
from app.sql_app.database import engine


def override_get_db():
    engine = create_engine(environ.get("DATABASE_URL"))
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session_local()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture(scope="function")
def client():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    # Override the dependency
    app.dependency_overrides[app.get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Clear overrides after the test
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def todo_factory(db: Session):
    def create(title, description):
        todo = ToDo(title=title, description=description)
        db.add(todo)
        db.flush()  # use flush to ensure ids are generated
        return todo

    return create


def test_get_todos_empty(client):
    # Test getting an empty list of todos
    response = client.get("/api/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_get_todos_with_todos(client, todo_factory):
    # Create todos
    todo_factory("Test Todo 1", "Test Description 1")
    todo_factory("Test Todo 2", "Test Description 2")
    todo_factory("Test Todo 3", "Test Description 3")

    # Test getting a list of todos
    response = client.get("/api/todos")
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 3
    assert todos[0]["title"] == "Test Todo 1"
    assert todos[1]["title"] == "Test Todo 2"
    assert todos[2]["title"] == "Test Todo 3"


def test_get_todos_with_pagination(client, todo_factory):
    # Create todos
    todo_factory("Test Todo 1", "Test Description 1")
    todo_factory("Test Todo 2", "Test Description 2")
    todo_factory("Test Todo 3", "Test Description 3")

    # Test getting todos with pagination
    response = client.get("/api/todos?skip=1&limit=2")
    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 2
    assert todos[0]["title"] == "Test Todo 2"
    assert todos[1]["title"] == "Test Todo 3"
