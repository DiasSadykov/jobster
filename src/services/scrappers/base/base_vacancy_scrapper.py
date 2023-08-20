import asyncio
from datetime import datetime, timedelta
import random
import httpx
from db.db import VacancyTable
from services.models import Vacancy
from services.reporting.telegram_reporting_service import TelegramReportingService

class VacancyScrapperBase:
    def __init__(self, url: str, source: str, log_tag: str, hour: int = 0, minute: int = 0, interval_hours: int = 12):
        self.source: str = source
        self.url_base: str = url
        self.client = httpx.AsyncClient()
        self.log_tag = log_tag
        self.hour = hour
        self.minute = minute
        self.interval_hours = interval_hours
        next_run_time = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
        if next_run_time < datetime.now():
            next_run_time = next_run_time.replace(day=next_run_time.day + 1)
        self.next_run_time = next_run_time

    async def scrap(self) -> list[Vacancy]:
        # take all vacancies from db in a set and then compare with new vacancies
        response = await self.client.get(self.url_base)
        vacancies = self.findData(response)
        return vacancies

    def save_in_db(self, vacancies):
        for vacancy in vacancies:
            VacancyTable.insert_vacancy(vacancy)

    async def _run(self):
        try:
            await TelegramReportingService.send_message_to_private_channel(f"[{self.log_tag}] Started Scrapping")
            old_vacancies = VacancyTable.get_by_source(self.source)
            old_vacancies_urls = set(vacancy.url for vacancy in old_vacancies)
            new_vacancies = await self.scrap()
            new_vacancies_dict = {vacancy.url: vacancy for vacancy in new_vacancies}
            new_vacancies_urls = set(vacancy.url for vacancy in new_vacancies)
            added_vacancies_urls = new_vacancies_urls - old_vacancies_urls
            added_vacancies = [new_vacancies_dict[url] for url in added_vacancies_urls]
            self.save_in_db(new_vacancies)
            await TelegramReportingService.send_message_to_private_channel(f"[{self.log_tag}] Saved {len(added_vacancies)} in db")
        except Exception as e:
            await TelegramReportingService.send_message_to_private_channel(f"[{self.log_tag}]: Error: {e}")

    async def run(self):
        while True:
            if datetime.now() < self.next_run_time:
                await asyncio.sleep(1)
                continue
            self.next_run_time = self.next_run_time + timedelta(hours=self.interval_hours)
            await self._run()

    async def run_now(self):
        await self._run()

    async def findData(self):
        raise NotImplementedError("Method findData is not implemented")
