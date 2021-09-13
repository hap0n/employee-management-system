from typing import Optional

from pydantic import BaseModel


class ProjectPosition(BaseModel):
    id: Optional[int]
    position_id: int
    reports_to: Optional[int]
