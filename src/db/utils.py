import os

from sqlmodel import Session, create_engine

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost:5432/techhunterdb", echo=True)

def get_session():
    with Session(engine) as session:
        yield session

