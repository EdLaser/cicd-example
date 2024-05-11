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


def test_get_todo(client, db: Session):
    # Test getting a todo
    todo = models.ToDo(title="Test Todo", description="Test Description")
    db.add(todo)
    db.commit()

    response = client.get(f"/api/todo/{todo.id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo"
    assert response.json()["description"] == "Test Description"
    assert response.json()["is_done"] is False

def test_get_todo_not_found(client, db: Session):
    # Test getting a todo that doesn't exist
    response = client.get("/api/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
