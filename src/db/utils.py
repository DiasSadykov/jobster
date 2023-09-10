import os

from sqlmodel import Session, create_engine

DATABASE_LOCATION = os.environ.get("DATABASE_LOCATION") or "db.sqlite3"
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
if DB_USER and DB_PASSWORD:
    engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/postgres", echo=True)
else:
    engine = create_engine(f"sqlite:///{DATABASE_LOCATION}", echo=True, connect_args={'check_same_thread': False})

def get_session():
    with Session(engine) as session:
        yield session

