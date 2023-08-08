import os
import telegram

from services.models import Vacancy

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = "-1001918708178"

PRIVATE_CHANNEL_ID = "-1001836766800"

class TelegramReportingService:
    @staticmethod
    async def send_message_to_public_channel(message, thread_id=None):
        bot = telegram.Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="HTML", disable_web_page_preview=True, reply_to_message_id=thread_id)

    @staticmethod
    async def send_message_to_private_channel(message):
        bot = telegram.Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=PRIVATE_CHANNEL_ID, text=message, parse_mode="HTML")

    @staticmethod
    def format_vacancy_with_link(vacancy: Vacancy):
        salary = vacancy.salary or "ЗП не указана"
        return f"<a href='{vacancy.url}'>{vacancy.title}, {salary}</a>"

    @staticmethod
    async def report_added_vacancies_by_company_sorted(vacancies: list[Vacancy]):
        if len(vacancies) == 0:
            message = "Сегодня новых вакансий нет, но посмотреть все вакансии можно на сайте: https://techhunter.kz/"
            await TelegramReportingService.send_message_to_public_channel(message, thread_id=141)
            return
        message = f"Новые вакансии: {len(vacancies)}\n\n"

        vacancies_by_company = {}
        for vacancy in vacancies:
            if vacancy.company not in vacancies_by_company:
                vacancies_by_company[vacancy.company] = []
            vacancies_by_company[vacancy.company].append(vacancy)
        
        # Sort by number of vacancies
        vacancies_by_company = dict(sorted(vacancies_by_company.items(), key=lambda item: len(item[1]), reverse=True))

        # limit number of companies to 5
        vacancies_by_company = dict(list(vacancies_by_company.items())[:5])

        for company, vacancies in vacancies_by_company.items():
            message += f"<b>{company}</b>\n"
            for vacancy in vacancies:
                message += TelegramReportingService.format_vacancy_with_link(vacancy)
                message += "\n"
            message += "\n"

        message += "\n"
        message += "Посмотреть все вакансии можно на сайте: https://techhunter.kz/"

        await TelegramReportingService.send_message_to_public_channel(message, thread_id=141)

    @staticmethod
    async def report_deleted_vacancies(vacancies: list[Vacancy]):
        message = f"{len(vacancies)} вакансий удалено\n"
        await TelegramReportingService.send_message_to_private_channel(message)
