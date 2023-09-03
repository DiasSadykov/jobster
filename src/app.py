import os
import uvicorn
from fastapi import FastAPI
from routers import user, company, vacancy

from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.include_router(user.router)
app.include_router(company.router)
app.include_router(vacancy.router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
