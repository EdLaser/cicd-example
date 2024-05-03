from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status

from .sql_app import crud, models, schemas
from .sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

TODO_NOT_FOUND="Todo not found"

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/new_todo", response_model=schemas.ToDo)
def create_user(todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(crud.create_todo(db=db, todo=todo)))


@app.get("/api", response_model=list[schemas.ToDo])
def get_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(todos))


@app.get("/api/todo/{todo_id}", response_model=schemas.ToDo)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(db_todo))

@app.put("/api/{todo_id}", response_model=schemas.ToDo)
def mark_as_done(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.update_todo_status(db, todo_id=todo_id, is_done=True)
    if db_todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(db_todo))

@app.delete("/api/delete/{todo_id}", response_model=schemas.ToDo)
def delete(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.delete_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(db_todo))
