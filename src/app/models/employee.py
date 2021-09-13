from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Employee(BaseModel):
    id: int
    first_name: str
    second_name: str
    date_of_birth: datetime
    gender: bool
    email: str
    salary: int
    position: str
    hired_on: datetime
    # TODO: add location

    reports_to: Optional[int] = None
