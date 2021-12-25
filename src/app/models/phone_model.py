from enum import Enum
from typing import Optional

from pydantic import BaseModel


class PhoneStatus(str, Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"


class Phone(BaseModel):
    id: Optional[int] = None
    status: PhoneStatus
    phone: str
    employee_id: int
