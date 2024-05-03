from pydantic import BaseModel


class ToDoBase(BaseModel):
    title: str
    description: str


class ToDoCreate(ToDoBase):
    title: str
    description: str


class ToDo(ToDoBase):
    id: int
    title: str
    description: str
    is_done: bool

    class Config:
        from_attributes = True
