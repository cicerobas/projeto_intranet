from sqlmodel import Session

from app.core.security import verify_password
from app.repositories.user import get_user_by_username


async def authenticate_user(session: Session, username: str, password: str):
    user = get_user_by_username(session, username)
    if not user or not verify_password(password, user.password):
        return False
    return user
