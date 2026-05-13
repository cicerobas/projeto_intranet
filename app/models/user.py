from sqlmodel import SQLModel, Field, JSON
from uuid import UUID, uuid4


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False)
    username: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    roles: list[str] = Field(default_factory=list, sa_type=JSON)
