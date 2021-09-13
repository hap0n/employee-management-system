from pydantic import BaseModel

from app.domains.user import Role


class User(BaseModel):
    id: int
    username: str
    role: Role = Role.user
