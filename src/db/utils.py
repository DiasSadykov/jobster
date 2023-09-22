import os

from sqlmodel import Session, create_engine

DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
ENV = os.environ.get("ENV") or "DEV"
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@localhost:5432/techhunterdb", echo=True if ENV == "DEV" else False, pool_size=100, max_overflow=20, pool_recycle=300)

def get_session():
    with Session(engine) as session:
        yield session
