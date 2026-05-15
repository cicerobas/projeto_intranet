from sqlmodel import Session, select

from app.models.role import Role


def get_role(session: Session, name: str) -> Role | None:
    return session.exec(select(Role).where(Role.name == name)).one_or_none()
