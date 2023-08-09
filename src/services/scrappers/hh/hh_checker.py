from services.models import Vacancy
from services.reporting.telegram_reporting_service import TelegramReportingService
from services.scrappers.base.base_vacancy_checker import VacancyCheckerBase
from bs4 import BeautifulSoup

MAX_PAGE = 100

class HHKZVacancyChecker(VacancyCheckerBase):
    def __init__(self):
        super().__init__("hh.kz")

    async def check_closed(self, vacancy: Vacancy):
        try:
            url = vacancy.url
            response = await self.client.get(vacancy.url, follow_redirects=True, timeout=2)
            if response.status_code != 200:
                TelegramReportingService.send_message_to_private_channel(f"[HH Checker] {response.status_code} on page {url}")
                return False
            soup = BeautifulSoup(response.text, 'html.parser')
            archive_description = soup.find("p", {"class": "vacancy-archive-description"})
            if archive_description:
                return True
            return False
        except Exception as e:
            TelegramReportingService.send_message_to_private_channel(f"[HH Checker] Error: {e}")
            return False