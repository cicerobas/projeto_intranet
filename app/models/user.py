from typing import TYPE_CHECKING

from sqlmodel import Relationship, SQLModel, Field
from uuid import UUID, uuid4

from app.models.user_role import UserRole

if TYPE_CHECKING:
    from app.models.role import Role


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False)
    username: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    is_active: bool = Field(default=True)

    roles: list["Role"] = Relationship(back_populates="users", link_model=UserRole)
