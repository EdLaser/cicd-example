import pytest
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.sql_app import models, schemas
from app.sql_app.crud import (
    get_todo,
    get_todos,
    create_todo,
    update_todo_status,
    delete_todo,
)


@pytest.fixture
def session():
    engine = create_engine(environ.get("DATABASE_URL"))
    models.Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    transaction = db.begin()  # Start a transaction
    try:
        yield db
    finally:
        transaction.rollback()  # Rollback all changes made in the session
        db.close()


def test_get_todo(session):
    # Create a sample todo
    todo = models.ToDo(title="Test Todo", description="Test Description")
    session.add(todo)
    session.flush()  # Use flush to assign an ID without committing

    # Test getting the todo by ID
    result = get_todo(session, todo.id)
    assert result.title == "Test Todo"
    assert result.description == "Test Description"

    # Test getting a todo that doesn't exist
    result = get_todo(session, 999)
    assert result is None


def test_get_todos(session):
    # Create multiple sample todos
    todos = [
        models.ToDo(title=f"Test Todo {i}", description=f"Test Description {i}")
        for i in range(3)
    ]
    session.add_all(todos)
    session.flush()  # Flush changes without committing

    # Test getting all todos
    result = get_todos(session)
    assert len(result) == 3

    # Test getting todos with pagination
    result = get_todos(session, skip=1, limit=2)
    assert len(result) == 2
    assert result[0].title == "Test Todo 1"
    assert result[1].title == "Test Todo 2"


def test_create_todo(session):
    # Test creating a todo
    todo = schemas.ToDoCreate(title="Test Todo", description="Test Description")
    result = create_todo(session, todo)
    assert result.title == "Test Todo"
    assert result.description == "Test Description"
    assert not result.is_done


def test_update_todo_status(session):
    # Create a sample todo
    todo = models.ToDo(title="Test Todo", description="Test Description")
    session.add(todo)
    session.flush()  # Flush to apply the ID

    # Test updating the todo status
    update_todo_status(session, todo.id, is_done=True)
    result = session.query(models.ToDo).filter_by(id=todo.id).first()
    assert result.is_done


def test_delete_todo(session):
    # Create a sample todo
    todo = models.ToDo(title="Test Todo", description="Test Description")
    session.add(todo)
    session.flush()  # Flush to apply the ID

    # Test deleting the todo
    delete_todo(session, todo.id)
    result = session.query(models.ToDo).filter_by(id=todo.id).first()
    assert result is None
