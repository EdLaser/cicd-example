import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)

from sqlalchemy.orm import declarative_base
from sqlalchemy import Boolean, Column, Integer, String

Base = declarative_base()


class ToDo(Base):
    """
    Represents a ToDo item within the database.

    Attributes:
        id (int): The primary key, an auto-incrementing integer that uniquely identifies a ToDo item.
        title (str): The title of the ToDo item.
        description (str): A more detailed description of the ToDo item.
        is_done (bool): A boolean flag indicating whether the ToDo item has been completed.
    """

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    is_done = Column(Boolean, default=False)
