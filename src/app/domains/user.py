from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Role(str, Enum):
    user = "user"
    hr = "hr"
    admin = "admin"


@dataclass
class User:
    username: str
    password_hash: str
    id: Optional[int] = None
    role: Role = Role.user
