from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status
from sqlmodel import Session

from app.core.dependencies import SessionDep
from app.core.security import verify_password, decode_access_token
from app.models.user import User
from app.repositories.user import get_user_by_username
from app.core.settings import get_settings

settings = get_settings()


async def authenticate_user(session: Session, username: str, password: str):
    user = get_user_by_username(session, username)
    if not user or not verify_password(password, user.password):
        return False
    return user


async def get_current_user(
    session: SessionDep, access_token: Annotated[str | None, Cookie()] = None
) -> User | None:
    if not access_token:
        return None

    payload = decode_access_token(access_token)
    if not payload:
        return None

    return session.get(User, payload.get("sub"))


def require_roles(*roles: str):
    def dependency(current_user: User = Depends(get_current_user)):
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        user_roles = {role.name for role in current_user.roles}
        if not user_roles.intersection(roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return current_user

    return dependency


def get_user_roles(current_user: User | None) -> list:
    if not current_user:
        return []
    return [role.name for role in current_user.roles]
