import os
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from db.user_table import UserTable
from db.vacancy_table import VacancyTable

from services.models import User, Vacancy
from services.reporting.telegram_reporting_service import TelegramReportingService

TEMPLATES_DIR = os.environ.get("TEMPLATES_DIR", "src/templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

class RecruiterService:
    def render_dashboard_page(self, request, user: User):
        if not user:
            return templates.TemplateResponse("login/login.html", {"request": request})
        return templates.TemplateResponse("dashboard/dashboard.html", {"request": request, "user": user, "page_title": "TechHunter - Кабинет Рекрутера"})

    async def post_vacancy(self, request: Request, user: User):
        if not user:
            return templates.TemplateResponse("login/login.html", {"request": request})
        if user.balance < 10000:
            return templates.TemplateResponse("dashboard/dashboard.html", {"request": request, "balance": user.balance, "error": "Недостаточно средств, пожалуйста пополните баланс"})
        request_data = await request.form()
        title = request_data.get("title")
        description = request_data.get("description")
        salary = request_data.get("salary")
        company = request_data.get("company")
        city = request_data.get("city")
        tags = request_data.get("tags")
        source = "techhunter.kz"
        vacancy = Vacancy(title=title, description=description, salary=salary, company=company, city=city, tags=tags, created_by=user.id, source=source)
        id = VacancyTable.insert_vacancy(vacancy)
        url = f"/vacancy/{id}"
        VacancyTable.update_url(id, url)
        user.balance -= 10000
        UserTable.update_user(user)
        await TelegramReportingService.send_message_to_private_channel(f"New vacancy posted: {title}")
        return RedirectResponse(f'/vacancy/{id}', status_code=303)
