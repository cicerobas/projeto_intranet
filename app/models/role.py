from typing import TYPE_CHECKING

from sqlmodel import Relationship, SQLModel, Field

from app.models.user_role import UserRole

if TYPE_CHECKING:
    from app.models.user import User


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False, max_length=20)

    users: list["User"] = Relationship(back_populates="roles", link_model=UserRole)
