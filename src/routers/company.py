from typing import Optional
from fastapi import APIRouter, Depends, Form, Request
from db.utils import get_session

from services.company_service import CompanyService

router = APIRouter()
company_service = CompanyService()

@router.get("/companies", tags=["companies"])
async def get_companies(request: Request, session = Depends(get_session)):
    return company_service.return_all_companies(request, session)

@router.get("/company/add", tags=["companies"])
async def get_company_add(request: Request):
    return company_service.render_add_new_company_form(request)

@router.get("/company/{id}", tags=["companies"])
async def get_company(request: Request, id: int, session = Depends(get_session)):
    return company_service.get_company(request, id, session)

@router.post("/company/add", tags=["companies"])
async def post_company_add(request: Request,
    name: str = Form(),
    description: Optional[str] = Form(None),
    headcount: Optional[str] = Form(None),
    type: Optional[str] = Form(None),
    industry: Optional[str] = Form(None),
    tech_stack: Optional[str] = Form(None),
    logo_url: Optional[str] = Form(None),
    website_url: Optional[str] = Form(None),
    session = Depends(get_session)
    ):
    return await company_service.add_new_company(
        request,
        name,
        description,
        headcount,
        type,
        industry,
        tech_stack,
        logo_url,
        website_url,
        session
    )
