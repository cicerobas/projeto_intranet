from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.database import create_db_and_tables, create_default_admin
from app.core.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    create_default_admin()
    yield


app = FastAPI(lifespan=lifespan)


templates = Jinja2Templates(directory="app/views/templates")
app.mount("/static", StaticFiles(directory="app/views/static"), name="static")

settings = get_settings()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
