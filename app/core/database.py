from sqlmodel import SQLModel, Session, create_engine

from app.core.security import get_password_hash
from app.core.settings import get_settings
from app.repositories.user import get_user_by_username
from app.models.user import User

settings = get_settings()

engine = create_engine(settings.database_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def create_default_admin():
    with Session(engine) as session:
        admin = get_user_by_username(session, "admin")
        if not admin:
            session.add(
                User(
                    name="Administrador",
                    username="admin",
                    password=get_password_hash(settings.default_admin_password),
                    roles=["admin"],
                )
            )
            session.commit()
