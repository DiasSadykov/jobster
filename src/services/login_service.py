from datetime import timedelta
import os
import bcrypt
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi_login import LoginManager
from db.user_table import UserTable
from services.reporting.telegram_reporting_service import TelegramReportingService

SECRET = "super-secret-key"
TEMPLATES_DIR = os.environ.get("TEMPLATES_DIR", "src/templates")
COOKIE_NAME = "access_token"

manager = LoginManager(SECRET, '/login', use_cookie=True, cookie_name=COOKIE_NAME, default_expiry=timedelta(weeks=1))
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@manager.user_loader()
def query_user(email: str):
    return UserTable.get_user_by_email(email)

class LoginService:
    def render_signup_page(self, request, user):
        if user:
            return RedirectResponse("/dashboard", status_code=303)
        return templates.TemplateResponse("signup/signup.html", {"request": request})

    def render_login_page(self, request, user):
        if user:
            return RedirectResponse("/dashboard", status_code=303)
        return templates.TemplateResponse("login/login.html", {"request": request})


    async def handle_signup(self, request: Request):
        request_data = await request.form()
        email = request_data.get("email")
        password = request_data.get("password")
        if not email or not password:
            return templates.TemplateResponse("signup/signup.html", {"request": request, "error": "Email and password are required"})
        # hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            id = UserTable.insert_user(email, hashed_password)
        except Exception as e:
            return templates.TemplateResponse("signup/signup.html", {"request": request, "error": "Пользователь с таким email уже существует"})
        access_token = manager.create_access_token(
            data={'sub': email}
        )
        await TelegramReportingService.send_message_to_private_channel(f"New user registered: {email}")
        response = RedirectResponse("/dashboard", status_code=303)
        response.set_cookie("access_token", access_token)
        return response

    async def handle_login(self, request: Request):
        request_data = await request.form()
        email = request_data.get("email")
        password = str(request_data.get("password"))
        if not email or not password:
            return templates.TemplateResponse("signup/signup.html", {"request": request, "error": "Email and password are required"})

        user = UserTable.get_user_by_email(email)

        if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password): 
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
