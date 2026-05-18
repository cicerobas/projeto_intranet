from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.core.database import create_db_and_tables, create_default_admin
from app.core.utils import templates
from app.routers import auth, user, role
from app.services.auth import get_current_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    create_default_admin()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/views/static"), name="static")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(role.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    messages = {
        401: "Você precisa estar logado para acessar essa página.",
        403: "Você não tem permissão para acessar essa página.",
        404: "Página não encontrada.",
    }
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        status_code=exc.status_code,
        context={
            "status_code": exc.status_code,
            "message": messages.get(exc.status_code, "Ocorreu um erro inesperado."),
        },
    )


@app.get("/", response_class=HTMLResponse, name="index")
def index(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": current_user,
            "user_roles": [role.name for role in current_user.roles]
            if current_user
            else [],
        },
    )
