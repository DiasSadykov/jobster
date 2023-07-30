import asyncio
import datetime
import time
import schedule
from db.db import VacancyTable
from services.reporting.telegram_reporting_service import TelegramReportingService

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

def run_reporting_cron():
    try:
        vacancies = VacancyTable.get_new_vacancies()
        loop.run_until_complete(TelegramReportingService.report_added_vacancies_by_company_sorted(vacancies))
        VacancyTable.set_new_vacancies_false()
    except Exception as e:
        loop.run_until_complete(TelegramReportingService.send_message_to_private_channel(f"Error in reporting cron: {e}"))

if __name__ == "__main__":
    schedule.every().day.at("15:00:00").do(run_reporting_cron)
    while True:
        schedule.run_pending()
        time.sleep(1)

