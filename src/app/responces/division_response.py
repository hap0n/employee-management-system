from typing import List

from pydantic import BaseModel

from app.models.division_model import DivisionStatus
from app.models.team_model import Team


class DivisionResponse(BaseModel):
    id: int
    status: DivisionStatus
    name: str

    lead_id: int
    teams: List[Team]
    document_ids: List[int]
