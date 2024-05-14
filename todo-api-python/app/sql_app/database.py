from contextlib import contextmanager
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://mysecretuser:mysecretpassword@localhost/todos"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def get_db():
    if os.getenv("RUN_APP", "False").lower() in ("true", "1", "t"):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:

        class MockDB:
            def close(self):
                pass

        yield MockDB()
