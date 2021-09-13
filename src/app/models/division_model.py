from enum import Enum
from typing import Optional

from pydantic import BaseModel


class DivisionStatus(str, Enum):
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"
    GATHERING = "gathering"
    CANCELLED = "cancelled"


class Division(BaseModel):
    id: Optional[int]
    status: DivisionStatus
    name: str

    lead_id: int
