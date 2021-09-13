from pydantic import BaseModel
from app.models.team import Team
from app.models.employee import Employee
from app.models.division import Division
from typing import List


class Company(BaseModel):
    id: int
    name: str
    lead: Employee
    divisions: List[Division]
    employers: List[Employee]
    teams: List[Team]
