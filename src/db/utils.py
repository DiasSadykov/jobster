import os

from sqlmodel import Session, create_engine

DATABASE_LOCATION = os.environ.get("DATABASE_LOCATION") or "db.sqlite3"
engine = create_engine(f"sqlite:///{DATABASE_LOCATION}", echo=True, connect_args={'check_same_thread': False})

def get_session():
    with Session(engine) as session:
        yield session

