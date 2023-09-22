from datetime import timedelta
import os
import bcrypt
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi_login import LoginManager
from sqlmodel import Session, select
from db.utils import engine
from models.sqlmodels import User, UserType
from services.reporting.telegram_reporting_service import TelegramReportingService

SECRET = "super-secret-key"
TEMPLATES_DIR = os.environ.get("TEMPLATES_DIR", "src/templates")
COOKIE_NAME = "access_token"

manager = LoginManager(SECRET, '/login', use_cookie=True, cookie_name=COOKIE_NAME, default_expiry=timedelta(weeks=1))
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@manager.user_loader()
def query_user(email: str):
    with Session(engine) as session:
        connection_pool = engine.pool
        print(f"Request user by email {email}", flush=True)
        print("Connection pool status1: " + connection_pool.status(), flush=True)

        user = session.query(User).filter(User.email == email).first()
        return user

class LoginService:
    def render_signup_page(self, request, user_type: str, user: User):
        if user:
            if user.user_type == UserType.recruiter:
                return RedirectResponse("/dashboard", status_code=303)
            else:
                return RedirectResponse("/", status_code=303)
        return templates.TemplateResponse("signup/signup.html", {"request": request, "user_type": user_type})

    def render_login_page(self, request, user):
        if user:
            return RedirectResponse("/dashboard", status_code=303)
        return templates.TemplateResponse("login/login.html", {"request": request})


    async def handle_signup(self, request: Request, session: Session):
        request_data = await request.form()
        email = request_data.get("email")
        password = request_data.get("password")
        user_type = request_data.get("user_type")
        if user_type not in UserType.__members__: 
            return templates.TemplateResponse("signup/signup.html", {"request": request, "error": "Invalid user type"})
        if not email or not password:
            return templates.TemplateResponse("signup/signup.html", {"request": request, "error": "Email and password are required"})
        # hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            user = User(email=email, password=hashed_password, user_type=UserType[user_type])
            session.add(user)
            session.commit()
        except Exception as e:
            return templates.TemplateResponse("signup/signup.html", {"request": request, "error": "Пользователь с таким email уже существует", "user_type": user_type})
        access_token = manager.create_access_token(
            data={'sub': email}
        )
        await TelegramReportingService.send_message_to_private_channel(f"New {user.user_type} registered: {email}")
        response = RedirectResponse("/dashboard" if user.user_type == UserType.recruiter else "/", status_code=303)
        response.set_cookie("access_token", access_token)
        return response

    async def handle_login(self, request: Request, session: Session):
        request_data = await request.form()
        email = request_data.get("email")
        password = str(request_data.get("password"))
        if not email or not password:
            return templates.TemplateResponse("signup/signup.html", {"request": request, "error": "Email and password are required"})

        user = session.exec(select(User).where(User.email == email)).first()
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf8')): 
            return templates.TemplateResponse("login/login.html", {"request": request, "error": "Неверный логин или пароль"})
        access_token = manager.create_access_token(
            data={'sub': email}
        )
        response = RedirectResponse("/dashboard", status_code=303)
        response.set_cookie(COOKIE_NAME, access_token)
        return response

    def handle_logout(self, _: Request):
        response = RedirectResponse("/", status_code=303)
        response.delete_cookie(COOKIE_NAME)
        return response
