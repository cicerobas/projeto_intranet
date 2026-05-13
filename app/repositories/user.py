from uuid import UUID

from sqlmodel import Session, select

from app.models.user import User


def get_user_by_username(session: Session, username: str) -> User | None:
    return session.exec(select(User).where(User.username == username)).one_or_none()


def get_user_by_id(session: Session, user_id: UUID) -> User | None:
    return session.get(User, user_id)
