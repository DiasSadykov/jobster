from fastapi import APIRouter
from fastapi import Depends, Request
from fastapi.responses import HTMLResponse
from services.login_service import manager
from services.recruiter_service import RecruiterService
from services.templating_service import TemplatingService

router = APIRouter()
templating_service = TemplatingService()
recruiter_service = RecruiterService()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templating_service.render_root_page(request)

@router.get("/jobs/{description}", response_class=HTMLResponse)
async def post_vacancy(request: Request, description: str):
    return templating_service.render_jobs_page(request, description)

@router.get("/vacancy/{id}", response_class=HTMLResponse)
async def get_vacancy(request: Request, id: int):
    return templating_service.render_vacancy(request, id)

@router.post("/post_vacancy", response_class=HTMLResponse)
async def post_vacancy(request: Request, user=Depends(manager.optional)):
    return await recruiter_service.post_vacancy(request, user)