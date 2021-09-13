from typing import List, Optional

from pydantic import BaseModel

from app.models.employee import Employee


class Team(BaseModel):
    id: int
    name: str
    lead: Employee

    employers: Optional[List[Employee]] = None
