import pytest
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sql_app.models import ToDo
from sql_app.models import Base

@pytest.fixture
def session():
    engine = create_engine(environ.get("DATABASE_URL"))
    Base.metadata.create_all(engine)
    session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=engine)
    db = session_local()
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


def test_get_todo(session):
    # Create a sample todo
    todo = ToDo(title="Test Todo", description="Test Description")
    session.add(todo)
    session.commit()

    # Test getting the todo by ID
    result = session.query(ToDo).get(todo.id)
    assert result.title == "Test Todo"
    assert result.description == "Test Description"

    # Test getting a todo that doesn't exist
    result = session.query(ToDo).get(999)
    assert result is None


def test_get_todos(session):
    # Create multiple sample todos
    todos = [
        ToDo(title=f"Test Todo {i}",
             description=f"Test Description {i}")
        for i in range(3)
    ]
    session.add_all(todos)
    session.commit()

    # Test getting all todos
    result = session.query(ToDo).all()
    assert len(result) == 3

    # Test getting todos with pagination
    result = session.query(ToDo).offset(1).limit(2).all()
    assert len(result) == 2
    assert result[0].title == "Test Todo 1"
    assert result[1].title == "Test Todo 2"
