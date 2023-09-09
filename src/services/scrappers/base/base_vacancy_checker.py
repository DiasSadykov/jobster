import asyncio
import httpx
from sqlmodel import Session
from models.sqlmodels import Vacancy
from db.utils import engine
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
                deleted_count = 0
                with Session(engine) as session:
                    all_vacancies = session.query(Vacancy).where(Vacancy.source == self.source).all()
                    for vacancy in all_vacancies:
                        if await self.check_closed(vacancy):
                            deleted_count += 1
                            session.delete(vacancy)
                        await asyncio.sleep(1)
                    session.commit()
                await TelegramReportingService.send_message_to_private_channel(f"[{self.source} checker]: Deleted {deleted_count} vacancies")
            except Exception as e:
                await TelegramReportingService.send_message_to_private_channel(f"[{self.source} checker]: Error: {e}")
            await TelegramReportingService.send_message_to_private_channel(f"[{self.source} checker]: {self.source} check finished")
            await asyncio.sleep(SCRAP_INTERVAL)

    async def run_now(self):
        pass

    async def check_closed(self, _):
        raise NotImplementedError("Method check_closed is not implemented")
