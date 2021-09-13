from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TeamStatus(str, Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    GATHERING = "gathering"


class Team(BaseModel):
    id: Optional[int]
    status: TeamStatus
    name: str
    lead_id: int
    division_id: int
