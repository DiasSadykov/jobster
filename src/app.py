import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from services.templating_service import TemplatingService
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return TemplatingService().render_root_page(request)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
