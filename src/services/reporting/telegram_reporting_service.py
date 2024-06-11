import os
from sqlmodel import Session
import telegram

from models.sqlmodels import Vacancy
from utils.salary import convert_salary_to_int

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ENV = os.environ.get("ENV")
CHANNEL_ID = "-1001918708178"

PRIVATE_CHANNEL_ID = "-1001836766800"

try:
    bot = telegram.Bot(token=BOT_TOKEN)
except telegram.error.InvalidToken as e:
    if ENV == "PROD":
        raise e

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
            if ENV == "PROD":
                await bot.send_message(chat_id=PRIVATE_CHANNEL_ID, text=message, parse_mode="HTML", disable_web_page_preview=True)
            else:
                print(message)
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def format_vacancy_with_link(vacancy: Vacancy):
        salary = vacancy.salary or ""
        return f"<a href='{vacancy.url}'>{vacancy.title} {salary}</a>"

    @staticmethod
    def group_vacancies_by_tags(vacancies: list[Vacancy]):
        tags = [
            "qa",
            "ios",
            "android",
            "frontend",
            "backend",
            "fullstack",
            "data",
            "design",
            "product",
            "python",
            "java_",
            "javascript",
        ]
        vacancies_by_tags = {}
        for tag in tags:
            vacancies_by_tags[tag] = []
        for vacancy in vacancies:
            for tag in tags:
                if vacancy.tags and tag in vacancy.tags.split(","):
                    vacancies_by_tags[tag].append(vacancy)
        return vacancies_by_tags

    @staticmethod
    async def report_added_vacancies_by_company_sorted(session: Session, private=False):
        vacancies = session.query(Vacancy).filter(Vacancy.is_new == True).all()
        if len(vacancies) == 0:
            message = "Сегодня новых вакансий нет, но посмотреть все вакансии можно на сайте: https://techhunter.kz/"
            if private:
                await TelegramReportingService.send_message_to_private_channel(message)
            else:
                await TelegramReportingService.send_message_to_public_channel(message, thread_id=141)
            return
        message = f"<b>Новые вакансии: {len(vacancies)} 🚀</b>\n\n"
        vacancies.sort(key=lambda vacancy: convert_salary_to_int(vacancy.salary), reverse=True)
        vacancies_by_tags: dict[str, list[Vacancy]] = TelegramReportingService.group_vacancies_by_tags(vacancies, )
        for tag, vacancies in vacancies_by_tags.items():
            if len(vacancies) == 0:
                continue
            message += f"<b>{tag.upper()}</b>: {len(vacancies)}\n"
            for vacancy in vacancies[:3]:
                message += TelegramReportingService.format_vacancy_with_link(vacancy)
                message += "\n"
            message += "\n"
        message += "\n"
        message += "Посмотреть остальные новые вакансии можно на сайте:\n https://techhunter.kz/"

        if private:
            await TelegramReportingService.send_message_to_private_channel(message)
        else:
            await TelegramReportingService.send_message_to_public_channel(message, thread_id=141)

    @staticmethod
    async def report_deleted_vacancies(vacancies: list[Vacancy]):
        message = f"{len(vacancies)} вакансий удалено\n"
        await TelegramReportingService.send_message_to_private_channel(message)
