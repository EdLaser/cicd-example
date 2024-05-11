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


def test_delete_todo(client, db: Session):
    # Test deleting a todo
    todo = models.ToDo(title="Test Todo", description="Test Description")
    db.add(todo)
    db.commit()

    response = client.delete(f"/api/{todo.id}")
    assert response.status_code == 200
    deleted_todo = response.json()
    assert deleted_todo["title"] == "Test Todo"
    assert deleted_todo["description"] == "Test Description"
    assert deleted_todo["is_done"] is False
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == todo.id).first()
    assert db_todo is None


def test_delete_todo_not_found(client, db: Session):
    # Test deleting a todo that doesn't exist
    response = client.delete("/api/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
