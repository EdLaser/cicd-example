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


def test_update_todo(client, db: Session):
    # Test updating a todo
    todo = models.ToDo(title="Test Todo", description="Test Description")
    db.add(todo)
    db.commit()

    todo_data = {
        "title": "Updated Test Todo",
        "description": "Updated Test Description",
        "is_done": True,
    }
    response = client.put(f"/api/{todo.id}", json=todo_data)
    assert response.status_code == 200
    updated_todo = response.json()
    assert updated_todo["title"] == "Updated Test Todo"
    assert updated_todo["description"] == "Updated Test Description"
    assert updated_todo["is_done"] is True
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == todo.id).first()
    assert db_todo is not None
    assert db_todo.title == "Updated Test Todo"


def test_update_todo_not_found(client, db: Session):
    # Test updating a todo that doesn't exist
    todo_data = {
        "title": "Updated Test Todo",
        "description": "Updated Test Description",
        "is_done": True,
    }
    response = client.put("/api/999", json=todo_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}