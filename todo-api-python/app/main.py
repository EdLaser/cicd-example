import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

TODO_NOT_FOUND = "Todo not found"


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def setup_routes(app):

    @app.post("/api/new_todo", response_model=schemas.ToDo)
    def create_todo(todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
        """
        Creates a new todo item.

        Parameters:
        - todo: schemas.ToDoCreate: The todo item to be created.
        - db: Session = Depends(get_db): The database session.

        Returns:
        - JSONResponse: The response indicating successful creation of the todo item.
        """
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=jsonable_encoder(crud.create_todo(db=db, todo=todo)),
        )

    @app.get("/api", response_model=list[schemas.ToDo])
    def get_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        """
        Retrieves a list of todos from the database based on the specified skip and limit parameters.

        Parameters:
            skip (int): The number of todos to skip. Defaults to 0.
            limit (int): The maximum number of todos to retrieve. Defaults to 100.
            db (Session, optional): The database session. Defaults to Depends(get_db).

        Returns:
            JSONResponse: The response containing the list of todos.

        Raises:
            None
        """
        todos = crud.get_todos(db, skip=skip, limit=limit)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=jsonable_encoder(todos)
        )

    @app.get("/api/todo/{todo_id}", response_model=schemas.ToDo)
    def get_todo(todo_id: int, db: Session = Depends(get_db)):
        """
        Retrieves a todo item from the database based on the specified todo_id.

        Parameters:
            - todo_id (int): The ID of the todo item to retrieve.
            - db (Session, optional): The database session. Defaults to Depends(get_db).

        Returns:
            - JSONResponse: The response containing the retrieved todo item.

        Raises:
            - HTTPException: If the todo item with the specified ID is not found.
        """
        db_todo = crud.get_todo(db, todo_id=todo_id)
        if db_todo is None:
            raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=jsonable_encoder(db_todo)
        )

    @app.put("/api/{todo_id}", response_model=schemas.ToDo)
    def mark_as_done(todo_id: int, db: Session = Depends(get_db)):
        """
        Marks a todo item as done in the database.

        Parameters:
            - todo_id (int): The ID of the todo item to mark as done.
            - db (Session, optional): The database session. Defaults to Depends(get_db).

        Returns:
            - JSONResponse: The response indicating successful marking of the todo item as done.

        Raises:
            - HTTPException: If the todo item with the specified ID is not found.
        """
        db_todo = crud.update_todo_status(db, todo_id=todo_id, is_done=True)
        if db_todo is None:
            raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=jsonable_encoder(db_todo)
        )

    @app.delete("/api/delete/{todo_id}", response_model=schemas.ToDo)
    def delete(todo_id: int, db: Session = Depends(get_db)):
        """
        Delete a todo item from the database.

        Parameters:
            - todo_id (int): The ID of the todo item to delete.
            - db (Session, optional): The database session. Defaults to Depends(get_db).

        Returns:
            - JSONResponse: The response indicating the deleted todo item.

        Raises:
            - HTTPException: If the todo item with the specified ID is not found.
        """
        db_todo = crud.delete_todo(db, todo_id=todo_id)
        if db_todo is None:
            raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=jsonable_encoder(db_todo)
        )


if __name__ == "__main__":
    setup_routes(app)
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
