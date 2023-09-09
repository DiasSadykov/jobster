import os

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from models.sqlmodels import Vacancy
from utils.salary import convert_salary_to_int
from utils.vacancies import calculate_promotion

TEMPLATES_DIR = os.environ.get("TEMPLATES_DIR", "src/templates")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

@dataclass
class Employer:
    db_name: str
    shown_name: str
    logo: str

TOP_EMPLOYERS = {
    "Kaspi.kz": Employer("Kaspi.kz", "Kaspi", "https://upload.wikimedia.org/wikipedia/ru/a/aa/Logo_of_Kaspi_bank.png"),
    "Публичная Компания «Freedom Finance Global PLC»": Employer("Публичная Компания «Freedom Finance Global PLC»", "Freedom Finance", "https://media.licdn.com/dms/image/C4E03AQH8L4nbgcSh5w/profile-displayphoto-shrink_800_800/0/1517371174271?e=2147483647&v=beta&t=U8cxozb4hxNRDqionRI569isxd3vtl3-6k0SggSlHHQ"),
    "Яндекс": Employer("Яндекс", "Yandex", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Yandex_icon.svg/2048px-Yandex_icon.svg.png"),
    "АО\xa0Колеса": Employer("АО\xa0Колеса", "Колеса", "https://avatars.dzeninfra.ru/get-zen-logos/246004/pub_5b8f90f730712100ab841ac1_5b8f919f78944e00aa281d9e/xxh"),
    "ТОО\xa0inDrive": Employer("ТОО\xa0inDrive", "inDrive", "https://is1-ssl.mzstatic.com/image/thumb/Purple126/v4/50/94/ab/5094ab3d-0a81-7c5d-0311-4205a7fa6821/AppIcon-0-0-1x_U007emarketing-0-5-0-0-85-220.png/1200x630wa.png"),
    "ТОО\xa0AVIATA.KZ": Employer("ТОО\xa0AVIATA.KZ", "Aviata.kz", "https://play-lh.googleusercontent.com/OL3avfQvT_bmskEIkuqeopTHfcP5PosPf8ndu_vs2X8hvG3uDclVcbL-FYJS6D46ZFI=w480-h960-rw")
}

job_tag_to_localized_job_title = {
    "frontend": "Frontend",
    "backend": "Backend",
    "fullstack": "Fullstack",
    "qa": "QA",
    "ios": "iOS",
    "android": "Android",
    "product": "Product",
    "data": "Data",
    "design": "Design",
    "analyst": "Analyst",
    "sysadmin": "Системный Администратор",
    "devops": "DevOps",
    "golang": "Golang",
    "python": "Python",
    "java_": "Java",
    "php": "PHP",
    "javascript": "JavaScript",
    "react": "React"
}

city_tag_to_localized_city_title = {
    "almaty": "Алматы",
    "astana": "Астана"
}


class TemplatingService:
    def get_all_vacancies_sorted(self, session: Session):
        all_vacancies = session.query(Vacancy).all()
        all_vacancies.sort(key=lambda vacancy: (calculate_promotion(vacancy)+convert_salary_to_int(vacancy.salary)), reverse=True)
        return all_vacancies

    def get_top_vacancies_by_company(self, all_vacancies: list[Vacancy]):
        top_vacancies = defaultdict(list)
        for vacancy in all_vacancies:
            if vacancy.company in TOP_EMPLOYERS:
                top_vacancies[vacancy.company].append(vacancy)
        return top_vacancies

    def format_vacancies(self, vacancies: list[Vacancy]):
        for vacancy in vacancies:
            if vacancy.source == "techhunter.kz":
                vacancy.title = "🔥 " + vacancy.title
            if vacancy.created_at > datetime.now() - timedelta(days=1):
                vacancy.title = "🆕 " + vacancy.title
                if vacancy.tags:
                    vacancy.tags += ",new"
                else:
                    vacancy.tags = "new"
        return vacancies
        

    def render_root_page(self, request, session: Session):
        all_vacancies = self.get_all_vacancies_sorted(session)
        all_vacancies = self.format_vacancies(all_vacancies)
        top_vacancies_by_company = self.get_top_vacancies_by_company(all_vacancies)
        return templates.TemplateResponse("index.html", {"request": request, 
                                                         "top_employers": TOP_EMPLOYERS.values(), 
                                                         "top_vacancies_by_company": top_vacancies_by_company, 
                                                         "all_vacancies": all_vacancies})

    def translate_description_into_city_and_job_title(self, description: str):
        [job_tag, city_tag] = description.split("-")[1:]
        city_tag = city_tag.strip()
        job_tag = job_tag.strip()
        if job_tag == "java":
            job_tag = "java_"
        job_title = job_tag_to_localized_job_title.get(job_tag, job_tag)
        city_title = city_tag_to_localized_city_title.get(city_tag, city_tag)
        return [city_title, job_title, job_tag]


    def render_jobs_page(self, request, description: str):
        all_vacancies = self.get_all_vacancies_sorted()
        all_vacancies = self.format_vacancies(all_vacancies)
        [city_title, job_title, job_tag] = self.translate_description_into_city_and_job_title(description)
        return templates.TemplateResponse("jobs_with_description.html", {"request": request, 
                                                         "all_vacancies": all_vacancies, "page_title": f"Вакансии {job_title} в {city_title}", "city_title": city_title, "job_title": job_title, "job_tag": job_tag})

    def render_vacancy(self, request, id: int, session: Session):
        vacancy = session.query(Vacancy).filter(Vacancy.id == id).first()
        return templates.TemplateResponse("vacancy.html", {"request":request, "vacancy": vacancy})
