from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class EmployeeStatus(str, Enum):
    WORKS = "works"
    BLACKLIST = "blacklist"
    FIRED = "fired"


class Employee(BaseModel):
    id: Optional[int]
    first_name: str
    middle_name: Optional[str]
    last_name: str
    info: Optional[str]
    date_of_birth: Optional[date]
    project_position_id: Optional[int]
    internal_position_id: Optional[int]
    hired_on: date
    fired_on: Optional[date]
    status: EmployeeStatus
