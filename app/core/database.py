from sqlmodel import SQLModel, Session, create_engine

from app.core.security import get_password_hash
from app.core.settings import get_settings
from app import models
from app.repositories.user import get_user_by_username
from app.repositories.role import get_role


settings = get_settings()

engine = create_engine(settings.database_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def create_default_admin():
    with Session(engine) as session:
        admin_role = get_role(session, "admin")
        if not admin_role:
            admin_role = models.Role(name="admin")
            session.add(admin_role)
            session.commit()
            session.refresh(admin_role)

        admin_user = get_user_by_username(session, "admin")
        if not admin_user:
            session.add(
                models.User(
                    name="Administrador",
                    username="admin",
                    password=get_password_hash(settings.default_admin_password),
                    roles=[admin_role],
                )
            )
            session.commit()
