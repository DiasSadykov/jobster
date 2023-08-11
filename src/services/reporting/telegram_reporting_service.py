import os
import telegram
from db.db import VacancyTable

from services.models import Vacancy
from utils.salary import convert_salary_to_int
from utils.vacancies import group_vacancies_by_company

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = "-1001918708178"

PRIVATE_CHANNEL_ID = "-1001836766800"

bot = telegram.Bot(token=BOT_TOKEN)

class TelegramReportingService:
    @staticmethod
    async def send_message_to_public_channel(message, thread_id=None):
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="HTML", disable_web_page_preview=True, reply_to_message_id=thread_id)
        except Exception as e:
            TelegramReportingService.send_message_to_private_channel(f"Error in sending message to public channel: {e}")

    @staticmethod
    async def send_message_to_private_channel(message):
        try:
            await bot.send_message(chat_id=PRIVATE_CHANNEL_ID, text=message, parse_mode="HTML", disable_web_page_preview=True)
        except Exception as e:
            pass

    @staticmethod
    def format_vacancy_with_link(vacancy: Vacancy):
        salary = vacancy.salary or ""
        return f"<a href='{vacancy.url}'>{vacancy.title} {salary}</a>"

    @staticmethod
    async def report_added_vacancies_by_company_sorted():
        vacancies = VacancyTable.get_new_vacancies()
        if len(vacancies) == 0:
            message = "Сегодня новых вакансий нет, но посмотреть все вакансии можно на сайте: https://techhunter.kz/"
            await TelegramReportingService.send_message_to_public_channel(message, thread_id=141)
            return
        message = f"<b>Новые вакансии: {len(vacancies)} 🚀</b>\n\n"
        vacancies.sort(key=lambda vacancy: convert_salary_to_int(vacancy.salary), reverse=True)
        vacancies_by_company = group_vacancies_by_company(vacancies)
        vacancies_by_company = dict(sorted(vacancies_by_company.items(), key=lambda item: len(item[1]), reverse=True))
        vacancies_by_company = dict(list(vacancies_by_company.items())[:5])
        for company, vacancies in vacancies_by_company.items():
            message += f"<b>{company}</b>\n"
            for vacancy in vacancies[:3]:
                message += TelegramReportingService.format_vacancy_with_link(vacancy)
                message += "\n"
            message += "\n"

        message += "\n"
        message += "Посмотреть остальные вакансии можно на сайте:\n https://techhunter.kz/"

        await TelegramReportingService.send_message_to_private_channel(message)

    @staticmethod
    async def report_deleted_vacancies(vacancies: list[Vacancy]):
        message = f"{len(vacancies)} вакансий удалено\n"
        await TelegramReportingService.send_message_to_private_channel(message)
