# create SQL table
import os
import sqlite3
from sqlite3 import Error

DATABASE_LOCATION = os.environ.get("DATABASE_LOCATION") or "db.sqlite3"


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
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS vacancy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
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
    create_table(conn, create_table_sql)