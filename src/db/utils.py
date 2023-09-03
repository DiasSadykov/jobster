# create SQL table
import os
import sqlite3
from sqlite3 import Error

from sqlmodel import Session, create_engine

DATABASE_LOCATION = os.environ.get("DATABASE_LOCATION") or "db.sqlite3"
engine = create_engine(f"sqlite:///{DATABASE_LOCATION}", echo=True, connect_args={'check_same_thread': False})

def get_session():
    with Session(engine) as session:
        yield session

def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_LOCATION, check_same_thread=False)
    except Error as e:
        print(e)
    return conn

# Create table
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)

def create_db_if_not_exists():
    conn = create_connection()
    create_vacancy_table_sql = """
        CREATE TABLE IF NOT EXISTS vacancy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            created_by INTEGER,
            salary TEXT,
            company TEXT,
            city TEXT,
            url TEXT UNIQUE,
            source TEXT,
            is_new BOOLEAN NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            tags TEXT
        );
    """
    create_user_table_sql = """
            CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            balance INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
    """
    create_table(conn, create_vacancy_table_sql)
    create_table(conn, create_user_table_sql)

conn = create_connection()
