from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse

from app.core.dependencies import FormDataDep, SessionDep
from app.core.security import create_access_token
from app.core.utils import templates
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/token")
async def get_access_token(
    session: SessionDep, form_data: FormDataDep, response: Response
):
    user = await auth_service.authenticate_user(
        session, form_data.username, form_data.password
    )
    if not user:
        return HTMLResponse(
            '<p id="erro" class="has-text-danger">Usuário ou Senha incorretos</p>'
        )

    access_token = create_access_token({"sub": str(user.id)})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
    )

    response.headers["HX-Redirect"] = "/"
    return {}


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={"login": True}
    )


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.headers["HX-Redirect"] = "/"
    return {}
