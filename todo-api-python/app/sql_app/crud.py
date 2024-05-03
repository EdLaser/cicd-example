from sqlalchemy.orm import Session

from . import models, schemas


def get_todo(db: Session, todo_id: int):
    return db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ToDo).offset(skip).limit(limit).all()


def create_todo(db: Session, todo: schemas.ToDoCreate):
    db_todo = models.ToDo(title=todo.title, description=todo.description, is_done=False)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo_status(db: Session, todo_id: int, is_done: bool):
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    db_todo.is_done = is_done
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    db.delete(db_todo)
    db.commit()
    return 1
