import asyncio
import httpx
from db.db import VacancyTable
from services.models import Vacancy
from services.reporting.telegram_reporting_service import TelegramReportingService

SCRAP_INTERVAL = 60 * 60

class VacancyCheckerBase:
    def __init__(self, source: str):
        self.client = httpx.AsyncClient()
        self.source: str = source

    async def run(self):
        while True:
            await TelegramReportingService.send_message_to_private_channel(f"[{self.source} checker]: Checking {self.source}")
            try:
                all_vacancies = VacancyTable.get_by_source(self.source)
                for vacancy in all_vacancies:
                    if await self.check_closed(vacancy):
                        VacancyTable.delete_vacancy(vacancy.url)
                        await TelegramReportingService.send_message_to_private_channel(f"[{self.source} checker]: Vacancy {vacancy.title} is closed")
                    await asyncio.sleep(1)
            except Exception as e:
                await TelegramReportingService.send_message_to_private_channel(f"[{self.source} checker]: Error: {e}")
            await asyncio.sleep(SCRAP_INTERVAL)

    async def check_closed(self, _):
        raise NotImplementedError("Method check_closed is not implemented")
