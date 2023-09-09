from fastapi import APIRouter
from fastapi import Depends, Request
from fastapi.responses import HTMLResponse
from db.utils import get_session
from services.login_service import manager
from services.recruiter_service import RecruiterService
from services.templating_service import TemplatingService

router = APIRouter()
templating_service = TemplatingService()
recruiter_service = RecruiterService()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request, session=Depends(get_session)):
    return templating_service.render_root_page(request, session)

@router.get("/jobs/{description}", response_class=HTMLResponse)
async def post_vacancy(request: Request, description: str, session=Depends(get_session)):
    return templating_service.render_jobs_page(request, description, session)

@router.get("/vacancy/{id}", response_class=HTMLResponse)
async def get_vacancy(request: Request, id: int, session=Depends(get_session)):
    return templating_service.render_vacancy(request, id, session=session)

@router.post("/post_vacancy", response_class=HTMLResponse)
async def post_vacancy(request: Request, user=Depends(manager.optional), session=Depends(get_session)):
    return await recruiter_service.post_vacancy(request, user, session)