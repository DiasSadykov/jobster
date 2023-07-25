from collections import defaultdict
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates
from db.db import VacancyTable
from services.models import Employer

templates = Jinja2Templates(directory="/app/src/templates")



TOP_EMPLOYERS = [
    Employer("Kaspi.kz", "https://upload.wikimedia.org/wikipedia/ru/a/aa/Logo_of_Kaspi_bank.png"),
    Employer("Яндекс", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Yandex_icon.svg/2048px-Yandex_icon.svg.png"),
    Employer("Публичная Компания «Freedom Finance Global PLC»","https://media.licdn.com/dms/image/C4E03AQH8L4nbgcSh5w/profile-displayphoto-shrink_800_800/0/1517371174271?e=2147483647&v=beta&t=U8cxozb4hxNRDqionRI569isxd3vtl3-6k0SggSlHHQ"),
    Employer("АО\xa0Колеса", "https://avatars.dzeninfra.ru/get-zen-logos/246004/pub_5b8f90f730712100ab841ac1_5b8f919f78944e00aa281d9e/xxh"),
    Employer("ТОО\xa0Playrix", "https://mir-s3-cdn-cf.behance.net/user/276/e0150b1991629.58386106cd3f0.png"),
    Employer("ТОО\xa0inDrive", "https://is1-ssl.mzstatic.com/image/thumb/Purple126/v4/50/94/ab/5094ab3d-0a81-7c5d-0311-4205a7fa6821/AppIcon-0-0-1x_U007emarketing-0-5-0-0-85-220.png/1200x630wa.png")
]


class TemplatingService:
    def render_root_page(self, request):
        vacancies = VacancyTable.get_all_vacancies()
        new_vacancies = [vacancy for vacancy in vacancies if datetime.fromisoformat(vacancy.created_at) > datetime.now() - timedelta(days=1)]
        new_vacancies_by_company = defaultdict(list)
        for vacancy in new_vacancies:
            new_vacancies_by_company[vacancy.company].append(vacancy)
        new_vacancies_sorted_by_company = sorted(new_vacancies_by_company.values(), key=lambda x: len(x), reverse=True)
        vacancies_by_company = defaultdict(list)
        for vacancy in vacancies:
            vacancies_by_company[vacancy.company].append(vacancy)
        vacancies_sorted_by_company = sorted(vacancies_by_company.values(), key=lambda x: len(x), reverse=True)

        return templates.TemplateResponse("index.html", {"request": request, "top_employers": TOP_EMPLOYERS, "vacancies_by_company": vacancies_by_company, "vacancies_sorted_by_company": vacancies_sorted_by_company, "new_vacancies_sorted_by_company": new_vacancies_sorted_by_company})
