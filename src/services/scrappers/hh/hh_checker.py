from services.models import Vacancy
from services.scrappers.base.base_vacancy_checker import VacancyCheckerBase
from bs4 import BeautifulSoup

MAX_PAGE = 100

class HHKZVacancyChecker(VacancyCheckerBase):
    def __init__(self):
        super().__init__("hh.kz")

    async def check_closed(self, vacancy: Vacancy):
        url = vacancy.url
        response = await self.client.get(vacancy.url)
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code} on page {url}")
        soup = BeautifulSoup(response.text, 'html.parser')
        archive_description = soup.find("p", {"class": "vacancy-archive-description"})
        if archive_description:
            return True
        return False