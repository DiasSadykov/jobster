import os
from fastapi import Request
from sqlmodel import Session
from models.sqlmodels import Company
from fastapi.templating import Jinja2Templates

from services.reporting.telegram_reporting_service import TelegramReportingService

TEMPLATES_DIR = os.environ.get("TEMPLATES_DIR", "src/templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

class CompanyService:
    def return_all_companies(self, request: Request, session: Session):
        companies = session.query(Company).where(Company.reviwed_at != None).all()
        return templates.TemplateResponse("companies/all_companies.html", {"request": request, "companies": companies, "page_title": "Все IT компании Казахстана"})

    def render_add_new_company_form(self, request: Request):
        return templates.TemplateResponse("companies/add_new_company_form.html", {"request": request, "page_title": "TechHunter - Добавить компанию"})

    def get_company(self, request: Request, id: int, session: Session):
        company = session.query(Company).where(Company.id == id).first()
        return templates.TemplateResponse("companies/company.html", {"request": request, "company": company, "page_title": "Профиль IT компании " + company.name})

    async def add_new_company(self, request: Request,
            name: str,
            description: str,
            headcount: str,
            type: str,
            industry: str,
            tech_stack: str,
            logo_url: str,
            website_url: str,
            session: Session
        ):
        company = Company(
            name=name,
            description=description,
            headcount=headcount,
            type=type,
            industry=industry,
            tech_stack=tech_stack,
            logo_url=logo_url,
            website_url=website_url
        )
        session.add(company)
        session.commit()
        await TelegramReportingService.send_message_to_private_channel(f"[Company] New company added: {name}")
        return templates.TemplateResponse("companies/company_added_success.html", {"request": request})
