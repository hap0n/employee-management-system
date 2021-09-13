from datetime import date
from typing import Optional

from pydantic import BaseModel


class Holiday(BaseModel):
    id: Optional[int] = None
    date: date
    name: str
