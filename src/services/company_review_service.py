from fastapi import Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session
from models.sqlmodels import CompanyReview, User

COMPANY_REVIEW_QUESTIONS = {
    "salary": "Я доволен зарплатой",
    "work_schedule": "Я доволен рабочим графиком в компании",
    "remote_work": "Я могу выбирать откуда работать",
    "equipment": "Компания предоставляет всю необходимую технику для работы",
    "career": "Компания предоставляет возможность карьерного роста",
    "projects": "В компании интересные проекты",
    "tech_stack": "В компании используют современные технологии/стек",
    "management": "Мне нравится менеджмент компании",
    "recommend": "Я готов рекомендовать компанию друзьям"
}

class CompanyReviewService:
    async def save_company_review(self, request: Request, company_id: int, user: User, session: Session):
        # delete old review if exists
        old_review = session.query(CompanyReview).where(CompanyReview.company_id == company_id).where(CompanyReview.user_id == user.id).first()
        if old_review:
            session.delete(old_review)
            session.commit()

        review = {}
        form = await request.form()
        for key in COMPANY_REVIEW_QUESTIONS.keys():
            review[key] = int(form.get(key))

        user_id = user.id
        company_review = CompanyReview(
            company_id=company_id,
            user_id=user_id,
            review=review
        )
        session.add(company_review)
        session.commit()

        return HTMLResponse(
            content="""
                <div>
                    <h1>Спасибо за ваш отзыв!</h1>
                </div>
            """,
            status_code=200
        )

    @staticmethod
    def get_and_calculate_company_review(company_id: int, session: Session):
        reviews = session.query(CompanyReview).where(CompanyReview.company_id == company_id).all()
        if len(reviews) == 0:
            return None
        review = {}
        for key in COMPANY_REVIEW_QUESTIONS.keys():
            review[key] = 0
        for r in reviews:
            for key in COMPANY_REVIEW_QUESTIONS.keys():
                review[key] += r.review[key]
        for key in COMPANY_REVIEW_QUESTIONS.keys():
            review[key] = round(review[key] / len(reviews), 1)
        return len(reviews), review

    def get_company_review_questions():
        return COMPANY_REVIEW_QUESTIONS
