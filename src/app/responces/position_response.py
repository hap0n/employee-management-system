from typing import List, Optional

from pydantic import BaseModel

from app.models.internal_position_model import InternalPosition
from app.models.position_model import Position
from app.models.project_position_model import ProjectPosition


class ProjectPositionPathResponse(BaseModel):
    path: List[ProjectPosition]


class InternalPositionPathResponse(BaseModel):
    path: List[InternalPosition]


class InternalPositionResponse(BaseModel):
    id: int
    position: Position
    parent: Optional[Position]
    children: List[InternalPosition]


class ProjectPositionResponse(BaseModel):
    id: int
    position: Position
    parent: Optional[Position]
    children: List[ProjectPosition]
