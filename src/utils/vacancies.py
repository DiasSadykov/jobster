from collections import defaultdict
from services.models import Vacancy


def group_vacancies_by_company(vacancies: list[Vacancy]):
    vacancies_by_company = defaultdict(list)
    for vacancy in vacancies:
        vacancies_by_company[vacancy.company].append(vacancy)
    return vacancies_by_company