from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.core.dependencies import SessionDep
from app.core.utils import templates
from app.models.user import User
from app.repositories import role as role_repo
from app.services import auth as auth_service

router = APIRouter(prefix="/roles", tags=["Funções"])


@router.get("/", response_class=HTMLResponse, name="roles")
def users(
    request: Request,
    session: SessionDep,
    current_user: User = Depends(auth_service.require_roles("admin")),
):
    return templates.TemplateResponse(
        request=request,
        name="roles.html",
        context={
            "user": current_user,
            "user_roles": auth_service.get_user_roles(current_user),
            "roles": role_repo.get_all_roles(session),
        },
    )
