import os

from sqlmodel import Session, create_engine

DATABASE_LOCATION = os.environ.get("DATABASE_LOCATION") or "db.sqlite3"
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
if DB_USER and DB_PASSWORD:
    print(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@host.docker.internal:5432/techhunterdb")
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@host.docker.internal:5432/techhunterdb", echo=True)
else:
    engine = create_engine(f"sqlite:///{DATABASE_LOCATION}", echo=True, connect_args={'check_same_thread': False})

def get_session():
    with Session(engine) as session:
        yield session

