import asyncio
import datetime
import time
import schedule
from sqlmodel import Session
from db.utils import engine
from models.sqlmodels import Vacancy
from services.reporting.telegram_reporting_service import TelegramReportingService

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

def run_reporting_cron():
    try:
        with Session(engine) as session:
            loop.run_until_complete(TelegramReportingService.report_added_vacancies_by_company_sorted(session))
            session.query(Vacancy).update({Vacancy.is_new: False})
            session.commit()
    except Exception as e:
        loop.run_until_complete(TelegramReportingService.send_message_to_private_channel(f"Error in reporting cron: {e}"))

if __name__ == "__main__":
    schedule.every().day.at("15:00:00").do(run_reporting_cron)
    while True:
        schedule.run_pending()
        time.sleep(1)

