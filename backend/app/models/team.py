from pydantic import BaseModel
from app.models.employee import Employee
from typing import List


class Team(BaseModel):
    id: int
    name: str
    lead: Employee
    employers: List[Employee]
