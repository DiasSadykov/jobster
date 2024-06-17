import os
from fastapi.templating import Jinja2Templates
import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request
from routers import user, company, vacancy
from fastapi.middleware.gzip import GZipMiddleware

from services.login_service import manager

ENV = os.environ.get("ENV") or "DEV"
TEMPLATES_DIR = os.environ.get("TEMPLATES_DIR", "src/templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

if ENV == "PROD":
    sentry_sdk.init(
        dsn="https://fad90a96deef9d5a0e009d3d1075414f@o4505853118054400.ingest.sentry.io/4505853119299584",
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0
    )

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)
manager.useRequest(app)

app.include_router(user.router)
app.include_router(company.router)
app.include_router(vacancy.router)

@app.get("/cv-review")
def cv_review(request: Request):
    return templates.TemplateResponse("cv_review.html", {"request": request, "page_title": "Techhunter - CV Review"})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True if ENV == "DEV" else False)
