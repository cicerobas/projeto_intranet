from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.core.database import create_db_and_tables, create_default_admin
from app.core.utils import templates
from app.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    create_default_admin()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/views/static"), name="static")

app.include_router(auth.router)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
