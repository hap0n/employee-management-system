from typing import List, Optional

from pydantic import BaseModel

from app.models.division import Division
from app.models.employee import Employee
from app.models.team import Team


class Company(BaseModel):
    id: int
    name: str
    lead: Employee

    divisions: Optional[List[Division]] = None
    employers: Optional[List[Employee]] = None
    teams: Optional[List[Team]] = None
