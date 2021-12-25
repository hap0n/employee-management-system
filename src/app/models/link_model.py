from typing import Optional

from pydantic import BaseModel


class Link(BaseModel):
    id: Optional[int] = None
    name: Optional[str]
    link: str
    employee_id: int
