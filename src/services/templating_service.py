from collections import defaultdict
from datetime import datetime, timedelta
import re
from fastapi.templating import Jinja2Templates
from db.db import VacancyTable
from services.models import Employer, Vacancy

templates = Jinja2Templates(directory="/app/src/templates")



TOP_EMPLOYERS = {
    "Kaspi.kz": Employer("Kaspi.kz", "Kaspi", "https://upload.wikimedia.org/wikipedia/ru/a/aa/Logo_of_Kaspi_bank.png"),
    "Яндекс": Employer("Яндекс", "Yandex", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Yandex_icon.svg/2048px-Yandex_icon.svg.png"),
    "Публичная Компания «Freedom Finance Global PLC»": Employer("Публичная Компания «Freedom Finance Global PLC»", "Freedom Finance", "https://media.licdn.com/dms/image/C4E03AQH8L4nbgcSh5w/profile-displayphoto-shrink_800_800/0/1517371174271?e=2147483647&v=beta&t=U8cxozb4hxNRDqionRI569isxd3vtl3-6k0SggSlHHQ"),
    "АО\xa0Колеса": Employer("АО\xa0Колеса", "Колеса", "https://avatars.dzeninfra.ru/get-zen-logos/246004/pub_5b8f90f730712100ab841ac1_5b8f919f78944e00aa281d9e/xxh"),
    "ТОО\xa0Playrix": Employer("ТОО\xa0Playrix", "Playrix", "https://mir-s3-cdn-cf.behance.net/user/276/e0150b1991629.58386106cd3f0.png"),
    "ТОО\xa0inDrive": Employer("ТОО\xa0inDrive", "inDrive", "https://is1-ssl.mzstatic.com/image/thumb/Purple126/v4/50/94/ab/5094ab3d-0a81-7c5d-0311-4205a7fa6821/AppIcon-0-0-1x_U007emarketing-0-5-0-0-85-220.png/1200x630wa.png"),
    "ТОО\xa0AVIATA.KZ": Employer("ТОО\xa0AVIATA.KZ", "Aviata.kz", "https://play-lh.googleusercontent.com/OL3avfQvT_bmskEIkuqeopTHfcP5PosPf8ndu_vs2X8hvG3uDclVcbL-FYJS6D46ZFI=w480-h960-rw")
}


class TemplatingService:
    def convert_salary_to_int(self, salary: str) -> int:
        if not salary:
            return 0
        
        salary = salary.replace(' ', '')
        salary = salary.replace('\xa0', '')
        salary = salary.replace('\u202f', '')
        numbers = re.findall(r'\d+', salary)
        average_salary = sum(map(int, numbers)) // len(numbers)
        currency_symbol = salary[-1]
        currency_rates = {'₸': 0.0025, '₽': 0.014, '€': 1.17}
        if currency_symbol in currency_rates:
            average_salary *= currency_rates[currency_symbol]
        
        return average_salary

    def get_all_vacancies_sorted_by_salary(self):
        all_vacancies = VacancyTable.get_all_vacancies()
        all_vacancies.sort(key=lambda vacancy: self.convert_salary_to_int(vacancy.salary), reverse=True)
        return all_vacancies

    def get_top_vacancies_by_company(self, all_vacancies: list[Vacancy]):
        top_vacancies = defaultdict(list)
        for vacancy in all_vacancies:
            if vacancy.company in TOP_EMPLOYERS:
                top_vacancies[vacancy.company].append(vacancy)
        return top_vacancies

    def get_new_vacancies(self, all_vacancies: list[Vacancy]):
        new_vacancies = []
        today = datetime.now()
        for vacancy in all_vacancies:
            if datetime.fromisoformat(vacancy.created_at) > today - timedelta(days=1):
                new_vacancies.append(vacancy)
        return new_vacancies

    def render_root_page(self, request):
        all_vacancies = self.get_all_vacancies_sorted_by_salary()
        new_vacancies = self.get_new_vacancies(all_vacancies)
        top_vacancies_by_company = self.get_top_vacancies_by_company(all_vacancies)
        return templates.TemplateResponse("index.html", {"request": request, 
                                                         "top_employers": TOP_EMPLOYERS.values(), 
                                                         "top_vacancies_by_company": top_vacancies_by_company, 
                                                         "all_vacancies": all_vacancies, 
                                                         "new_vacancies": new_vacancies})
