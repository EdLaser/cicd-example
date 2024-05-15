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


def test_get_todo(client, todo_factory):
    # Create a todo using the factory
    todo = todo_factory("Test Todo", "Test Description")

    # Test getting the todo
    response = client.get(f"/api/todo/{todo.id}")
    assert response.status_code == 200
    todo_json = response.json()
    assert todo_json["title"] == "Test Todo"
    assert todo_json["description"] == "Test Description"
    assert todo_json["is_done"] is False


def test_get_todo_not_found(client):
    # Test getting a todo that doesn't exist
    response = client.get("/api/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
