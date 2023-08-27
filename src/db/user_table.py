from services.models import User
from db.utils import conn

FIELDS = "id, email, password, balance, created_at"

class UserTable:
    @staticmethod
    def insert_user(email: str, password: str):
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO user (email, password)
            VALUES (?, ?)
            """,
            (
             email,
             password
            )
        )
        conn.commit()
        cursor.close()
        return cursor.lastrowid

    @staticmethod
    def get_user_by_email(email: str) -> User:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {FIELDS} FROM user WHERE email=?", (email,))
        row = cursor.fetchone()
        cursor.close()
        return User(*row) if row else None

    @staticmethod
    def update_user(user: User):
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE user
            SET balance = ?
            WHERE id = ?
            """,
            (
             user.balance,
             user.id
            )
        )
        conn.commit()
        cursor.close()