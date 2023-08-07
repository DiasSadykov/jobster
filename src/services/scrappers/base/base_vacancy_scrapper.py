import asyncio
import httpx
from db.db import VacancyTable
from services.models import Vacancy
from services.reporting.telegram_reporting_service import TelegramReportingService

SCRAP_INTERVAL = 60 * 60 * 12

class VacancyScrapperBase:
    def __init__(self, url: str, source: str):
        self.source: str = source
        self.url_base: str = url
        self.client = httpx.AsyncClient()

    async def scrap(self) -> list[Vacancy]:
        # take all vacancies from db in a set and then compare with new vacancies
        response = await self.client.get(self.url_base)
        vacancies = self.findData(response)
        return vacancies

    def save_in_db(self, vacancies):
        for vacancy in vacancies:
            VacancyTable.insert_vacancy(vacancy)

    async def run(self):
        while True:
            await TelegramReportingService.send_message_to_private_channel(f"Scrapping {self.source}")
            try:
                old_vacancies = VacancyTable.get_by_source(self.source)
                old_vacancies_urls = set(vacancy.url for vacancy in old_vacancies)
                new_vacancies = await self.scrap()
                new_vacancies_dict = {vacancy.url: vacancy for vacancy in new_vacancies}
                new_vacancies_urls = set(vacancy.url for vacancy in new_vacancies)
                added_vacancies_urls = new_vacancies_urls - old_vacancies_urls
                added_vacancies = [new_vacancies_dict[url] for url in added_vacancies_urls]
                self.save_in_db(new_vacancies)
                await TelegramReportingService.send_message_to_private_channel(f"Saved {len(added_vacancies)} in db")
            except Exception as e:
                await TelegramReportingService.send_message_to_private_channel(f"Error in {self.source}: {e}")
            await asyncio.sleep(SCRAP_INTERVAL)

    async def findData(self):
        raise NotImplementedError("Method findData is not implemented")
