from pydantic import BaseModel
from datetime import datetime


class Employee(BaseModel):
    id: int
    first_name: str
    second_name: str
    date_of_birth: datetime
    gender: bool
    email: str
    salary: int
    reports_to: int
    position: str
    # TODO: add location
    hired_on: datetime
