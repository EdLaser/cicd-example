import pytest
from sqlalchemy.orm import Session
from sql_app.models import ToDo

@pytest.fixture
def session():
    db = Session()
    yield db
    db.close()

def test_create_todo(session):
    todo = ToDo(title="Test Todo", description="This is a test todo.")
    session.add(todo)
    session.commit()
    assert todo.id is not None
    assert todo.title == "Test Todo"
    assert todo.description == "This is a test todo."
    assert not todo.is_done

def test_update_todo(session):
    todo = ToDo(title="Test Todo", description="This is a test todo.")
    session.add(todo)
    session.commit()
    todo.title = "Updated Todo"
    session.commit()
    assert todo.title == "Updated Todo"

def test_delete_todo(session):
    todo = ToDo(title="Test Todo", description="This is a test todo.")
    session.add(todo)
    session.commit()
    session.delete(todo)
    session.commit()
    assert session.query(ToDo).filter_by(id=todo.id).first() is None