from typing import Optional

from pydantic import BaseModel


class InternalPosition(BaseModel):
    id: Optional[int]
    position_id: int
    reports_to: Optional[int]
