# write a class that will be used to scrap data from bolt website



from bs4 import BeautifulSoup
from services.models import Vacancy
from services.scrappers.base_vacancy_scrapper import VacancyScrapperBase


class BoltScrapper(VacancyScrapperBase):
    def __init__(self):
        super().__init__("https://bolt.eu/en-ua/careers/", "bolt.eu")

    async def findData(self, response):
        if response.status_code != 200:
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        vacancies_raw = soup.find_all("div", {"class": "job-listing"})
        vacancies = []
        for vacancy_raw in vacancies_raw:
            title_and_link = vacancy_raw.find("a", {"class": "job-listing-title"})
            title = title_and_link.text
            link = title_and_link.get("href")
            city = vacancy_raw.find("span", {"class": "job-listing-location"})
            if city:
                city = city.text.strip()
            else:
                city = None
            company = vacancy_raw.find("span", {"class": "job-listing-company"})
            if company:
                company = company.text.strip()
            else:
                company = None
            salary = None
            vacancies.append(Vacancy(title, link, salary, company, city, self.source))
        return vacancies
