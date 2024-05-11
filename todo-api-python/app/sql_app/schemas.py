from pydantic import BaseModel


class ToDoBase(BaseModel):
    title: str
    description: str


class ToDoCreate(ToDoBase):
    title: str
    description: str


class ToDo(ToDoBase):
    """
    Represents a ToDo item with additional metadata.

    Attributes:
        id (int): Unique identifier for the ToDo item.
        title (str): Title of the ToDo item.
        description (str): Detailed description of the ToDo item.
        is_done (bool): Status of the ToDo item, indicating completion.
    """

    id: int
    title: str
    description: str
    is_done: bool

    class Config:
        from_attributes = True
