from models.models import Vacancy
from db.utils import conn
FIELDS = "title, description, created_by, url, salary, company, city, source, is_new, created_at, id, tags"

class VacancyTable:
    @staticmethod
    def insert_vacancy(vacancy: Vacancy):
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO vacancy (title, description, created_by, url, salary, company, city, source, is_new, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                title = excluded.title,
                salary = excluded.salary,
                company = excluded.company,
                city = excluded.city,
                source = excluded.source,
                tags = excluded.tags
            """,
            (
             vacancy.title,
             vacancy.description,
             vacancy.created_by,
             vacancy.url,
             vacancy.salary,
             vacancy.company,
             vacancy.city,
             vacancy.source,
             vacancy.is_new,
             vacancy.tags
            )
        )
        conn.commit()
        cursor.close()
        return cursor.lastrowid

    def update_url(id: int, url: str):
        cursor = conn.cursor()
        cursor.execute("UPDATE vacancy SET url=? WHERE id=?", (url, id))
        conn.commit()
        cursor.close()

    @staticmethod
    def delete_vacancy(url: str):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vacancy WHERE url=?", (url,))
        conn.commit()
        cursor.close()

    @staticmethod
    def get_all_vacancies() -> list[Vacancy]:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {FIELDS} FROM vacancy")
        rows = cursor.fetchall()
        cursor.close()
        return [Vacancy(*row) for row in rows]

    @staticmethod
    def get_by_source(source: str) -> list[Vacancy]:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {FIELDS} FROM vacancy WHERE source=?", (source,))
        rows = cursor.fetchall()
        cursor.close()
        return [Vacancy(*row) for row in rows]

    @staticmethod
    def get_by_id(id: int) -> Vacancy:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {FIELDS} FROM vacancy WHERE id=?", (id,))
        row = cursor.fetchone()
        cursor.close()
        return Vacancy(*row) if row else None

    @staticmethod
    def get_new_vacancies() -> list[Vacancy]:
        cursor = conn.cursor()
        cursor.execute(f"SELECT {FIELDS} FROM vacancy WHERE is_new=1")
        rows = cursor.fetchall()
        cursor.close()
        return [Vacancy(*row) for row in rows]
    
    @staticmethod
    def set_new_vacancies_false():
        cursor = conn.cursor()
        cursor.execute("UPDATE vacancy SET is_new=0")
        conn.commit()
        cursor.close()