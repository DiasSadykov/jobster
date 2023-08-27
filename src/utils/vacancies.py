from collections import defaultdict
from services.models import Vacancy


def group_vacancies_by_company(vacancies: list[Vacancy]):
    vacancies_by_company = defaultdict(list)
    for vacancy in vacancies:
        vacancies_by_company[vacancy.company].append(vacancy)
    return vacancies_by_company

def calculate_promotion(vacancy: Vacancy):
    if vacancy.source == "techhunter.kz":
        return 10 ** 10
    if vacancy.created_by:
        return 10 ** 10
    return 0