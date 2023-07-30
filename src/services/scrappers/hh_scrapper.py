from .base_vacancy_scrapper import VacancyScrapperBase
from services.models import Vacancy
from bs4 import BeautifulSoup

MAX_PAGE = 100

class HHKZVacancyScrapper(VacancyScrapperBase):
    def __init__(self):
        super().__init__("https://hh.kz/vacancies/programmist?page={page}", "hh.kz")

    async def scrap_page(self, page) -> int:
        url = self.url_base.format(page=page)
        response = await self.client.get(url)
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code} on page {url}")
        return self.findData(response)

    async def scrap(self):
        vacancies = []
        for page in range(0, MAX_PAGE):
            try:
                vacancies.extend(await self.scrap_page(page))
            except:
                break
        return vacancies

    def findData(self, response):
        if response.status_code != 200:
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        vacancies_raw = soup.find_all("div", {"class": "vacancy-serp-item-body__main-info"})
        vacancies = []
        for vacancy_raw in vacancies_raw:
            title_and_link = vacancy_raw.find("a", {"class": "serp-item__title"})
            title = title_and_link.text
            link = title_and_link.get("href")
            city = vacancy_raw.find("div", {"data-qa": "vacancy-serp__vacancy-address"})
            if city:
                city = city.text.strip()
            else:
                city = None
            company = vacancy_raw.find("a", {"data-qa": "vacancy-serp__vacancy-employer"})
            if company:
                company = company.text.strip()
            else:
                company = None
            salary = vacancy_raw.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})
            if salary:
                salary = salary.text.strip()
            else:
                salary = None
            vacancies.append(Vacancy(title=title, url=link, salary=salary, company=company, city=city, source=self.source, is_new=True))
        return vacancies