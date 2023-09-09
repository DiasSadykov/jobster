import os
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from models.sqlmodels import User, Vacancy
from services.reporting.telegram_reporting_service import TelegramReportingService

TEMPLATES_DIR = os.environ.get("TEMPLATES_DIR", "src/templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

class RecruiterService:
    def render_dashboard_page(self, request, user: User):
        if not user:
            return templates.TemplateResponse("login/login.html", {"request": request})
        return templates.TemplateResponse("dashboard/dashboard.html", {"request": request, "user": user, "page_title": "TechHunter - Кабинет Рекрутера"})

    async def post_vacancy(self, request: Request, user: User, session: Session):
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
        session.add(vacancy)
        session.commit()
        vacancy.url = f"/vacancy/{vacancy.id}"
        user.balance -= 10000
        session.commit()
        await TelegramReportingService.send_message_to_private_channel(f"New vacancy posted: {title}")
        return RedirectResponse(f'/vacancy/{vacancy.id}', status_code=303)
