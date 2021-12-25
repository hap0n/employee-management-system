from enum import Enum
from typing import Optional

from pydantic import BaseModel


class PositionType(str, Enum):
    INTERNAL = "internal"
    PROJECT = "project"


class PositionStatus(str, Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"


class Position(BaseModel):
    id: Optional[int]
    status: PositionStatus
    name: str
