from typing import List

from pydantic import BaseModel

from app.models.team_model import TeamStatus


class TeamResponse(BaseModel):
    id: int
    status: TeamStatus
    name: str
    lead_id: int
    division_id: int

    employee_ids: List[int]
    document_ids: List[int]
