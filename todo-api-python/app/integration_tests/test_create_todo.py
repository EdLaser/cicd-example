import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app, get_db
from app.sql_app import crud, models, schemas
from app.sql_app.database import SessionLocal, engine


@pytest.fixture
def client():
    models.Base.metadata.create_all(bind=engine)
    with TestClient(app) as client:
        yield client


def test_create_todo(client: TestClient, session: Session):
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo"
    }
    response = client.post("/api/new_todo", json=todo_data)
    assert response.status_code == 201
    created_todo = response.json()
    assert created_todo["title"] == "Test Todo"
    assert created_todo["description"] == "This is a test todo"
    assert created_todo["is_done"] is False
    db_todo = session.query(models.ToDo).filter(
        models.ToDo.id == created_todo["id"]).first()
    assert db_todo is not None
    assert db_todo.title == "Test Todo"
    assert db_todo.description == "This is a test todo"
    assert not db_todo.is_done


def test_create_todo_missing_title(client: TestClient, session: Session):
    todo_data = {
        "description": "This is a test todo"
    }
    response = client.post("/api/new_todo", json=todo_data)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "title"],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


def test_create_todo_missing_description(client: TestClient, session: Session):
    todo_data = {
        "title": "Test Todo",
    }
    response = client.post("/api/new_todo", json=todo_data)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "description"],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
