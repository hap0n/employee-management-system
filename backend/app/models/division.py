from pydantic import BaseModel
from app.models.team import Team
from app.models.employee import Employee
from typing import List


class Division(BaseModel):
    id: int
    name: str
    lead: Employee
    employers: List[Employee]
    teams: List[Team]
