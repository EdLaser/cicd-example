import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)


from sqlalchemy.orm import Session

from . import models, schemas


def get_todo(db: Session, todo_id: int):
    """
    Retrieves a todo item from the database based on the specified todo_id.

    Parameters:
        db (Session): The database session.
        todo_id (int): The ID of the todo item to retrieve.

    Returns:
        ToDo | None: The todo item with the specified ID, or None if not found.
    """
    return db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of todos from the database based on the specified skip and limit parameters.

    Parameters:
        db (Session): The database session.
        skip (int): The number of todos to skip. Defaults to 0.
        limit (int): The maximum number of todos to retrieve. Defaults to 100.

    Returns:
        list: The list of todos retrieved from the database.
    """
    return db.query(models.ToDo).offset(skip).limit(limit).all()


def create_todo(db: Session, todo: schemas.ToDoCreate):
    """
    Creates a new todo item in the database.

    Parameters:
        db (Session): The database session.
        todo (schemas.ToDoCreate): The todo item to be created.

    Returns:
        models.ToDo: The newly created todo item.
    """
    db_todo = models.ToDo(title=todo.title, description=todo.description, is_done=False)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo_status(db: Session, todo_id: int, is_done: bool):
    """
    Updates the status of a todo item in the database.

    Parameters:
        - db (Session): The database session.
        - todo_id (int): The ID of the todo item to update.
        - is_done (bool): The new status of the todo item.

    Returns:
        - models.ToDo: The updated todo item.
    """
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    db_todo.is_done = is_done
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    """
    Deletes a todo item from the database based on the specified todo_id.

    Parameters:
        - db (Session): The database session.
        - todo_id (int): The ID of the todo item to delete.

    Returns:
        - int: 1 if the deletion was successful.
    """
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    db.delete(db_todo)
    db.commit()
    return 1
