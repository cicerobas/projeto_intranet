from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.core.utils import templates
from app.models.user import User
from app.services import auth as auth_service

router = APIRouter(prefix="/users", tags=["Usuários"])


@router.get("/", response_class=HTMLResponse)
def users(
    request: Request, current_user: User = Depends(auth_service.require_roles("admin"))
):
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={
            "user": current_user,
            "user_roles": [role.name for role in current_user.roles]
            if current_user
            else [],
        },
    )
