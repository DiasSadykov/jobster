from fastapi_login import LoginManager
import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from db.utils import create_connection
from services.login_service import LoginService, manager
from services.recruiter_service import RecruiterService
from services.templating_service import TemplatingService
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)

conn = create_connection()
templating_service = TemplatingService()
login_service = LoginService()
recruiter_service = RecruiterService()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templating_service.render_root_page(request)

@app.get("/vacancy/{id}", response_class=HTMLResponse)
async def get_vacancy(request: Request, id: int):
    return templating_service.render_vacancy(request, id)

@app.get("/signup", response_class=HTMLResponse)
def get_signup(request: Request, user=Depends(manager.optional)):
    return login_service.render_signup_page(request, user)

@app.post("/signup", response_class=HTMLResponse)
async def post_signup(request: Request):
    return await login_service.handle_signup(request)

@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request, user=Depends(manager.optional)):
    return login_service.render_login_page(request, user)

@app.post("/login", response_class=HTMLResponse)
async def post_login(request: Request):
    return await login_service.handle_login(request)

@app.post("/logout")
async def logout(request: Request):
    return login_service.handle_logout(request)

@app.get("/dashboard", response_class=HTMLResponse)
async def post_login(request: Request, user=Depends(manager.optional)):
    return recruiter_service.render_dashboard_page(request, user)

@app.post("/post_vacancy", response_class=HTMLResponse)
async def post_vacancy(request: Request, user=Depends(manager.optional)):
    return await recruiter_service.post_vacancy(request, user)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
