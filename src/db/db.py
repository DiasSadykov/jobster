import os
from db.utils import create_connection

from services.models import Vacancy

conn = create_connection()

class VacancyTable:
    @staticmethod
    def insert_vacancy(vacancy: Vacancy):
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO vacancy (title, url, salary, company, city, source)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                title = excluded.title,
                salary = excluded.salary,
                company = excluded.company,
                city = excluded.city,
                source = excluded.source
            """,
            (vacancy.title, vacancy.url, vacancy.salary, vacancy.company, vacancy.city, vacancy.source)
        )
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
        cursor.execute("SELECT title, url, salary, company, city, source, created_at FROM vacancy")
        rows = cursor.fetchall()
        cursor.close()
        return [Vacancy(*row) for row in rows]

    @staticmethod
    def get_by_source(source: str) -> list[Vacancy]:
        cursor = conn.cursor()
        cursor.execute("SELECT title, url, salary, company, city, source, created_at FROM vacancy WHERE source=?", (source,))
        rows = cursor.fetchall()
        cursor.close()
        return [Vacancy(*row) for row in rows]
