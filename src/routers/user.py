from fastapi import APIRouter
from fastapi import Depends, Request
from fastapi.responses import HTMLResponse
from db.utils import get_session
from services.login_service import LoginService, manager
from services.recruiter_service import RecruiterService

router = APIRouter()
login_service = LoginService()
recruiter_service = RecruiterService()


@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request, user=Depends(manager.optional)):
    return login_service.render_login_page(request, user)

@router.get("/signup", response_class=HTMLResponse)
def get_signup(request: Request, user_type:str, user=Depends(manager.optional)):
    return login_service.render_signup_page(request, user_type, user)

@router.post("/signup", response_class=HTMLResponse)
async def post_signup(request: Request, session=Depends(get_session)):
    return await login_service.handle_signup(request, session)

@router.post("/login", response_class=HTMLResponse)
async def post_login(request: Request, session=Depends(get_session)):
    return await login_service.handle_login(request, session)

@router.post("/logout")
async def logout(request: Request):
    return login_service.handle_logout(request)

@router.get("/dashboard", response_class=HTMLResponse)
async def post_login(request: Request, user=Depends(manager.optional)):
    return recruiter_service.render_dashboard_page(request, user)