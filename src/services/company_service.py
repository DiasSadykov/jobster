import os
from fastapi import Request
from sqlmodel import Session
from models.sqlmodels import Company, CompanyReview, User
from fastapi.templating import Jinja2Templates
from services.company_review_service import CompanyReviewService

from services.reporting.telegram_reporting_service import TelegramReportingService

TEMPLATES_DIR = os.environ.get("TEMPLATES_DIR", "src/templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

class CompanyService:
    def return_all_companies(self, request: Request, session: Session):
        companies: list[Company] = session.query(Company).where(Company.reviwed_at != None).all()
        company_reviews_averaged = CompanyReviewService.get_and_calculate_all_companies_reviews_by_company(session)
        companies_sorted_by_number_of_reviews = sorted(companies, key=lambda x: company_reviews_averaged.get(x.id, (0,0))[1], reverse=True)
        return templates.TemplateResponse("companies/all_companies.html", {"request": request, "companies": companies_sorted_by_number_of_reviews, "page_title": "Все IT компании Казахстана", "company_reviews_averaged": company_reviews_averaged})

    def render_add_new_company_form(self, request: Request):
        return templates.TemplateResponse("companies/add_new_company_form.html", {"request": request, "page_title": "TechHunter - Добавить компанию"})

    def get_company(self, request: Request, id: int, user: User, session: Session):
        company = session.query(Company).where(Company.id == id).first()
        own_company_review = session.query(CompanyReview).where(CompanyReview.company_id == id).where(CompanyReview.user_id == user.id).first() if user else None
        company_review_questions = CompanyReviewService.get_company_review_questions()
        len_reviews, company_review_summary = CompanyReviewService.get_and_calculate_company_review(id, session)
        return templates.TemplateResponse("companies/company.html", {"request": request, "company": company, "page_title": "Профиль IT компании " + company.name, "company_review_questions": company_review_questions, "own_company_review": own_company_review, "len_reviews": len_reviews, "company_review_summary": company_review_summary})

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
