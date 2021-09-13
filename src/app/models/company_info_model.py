from typing import Optional

from pydantic import BaseModel


class CompanyInfo(BaseModel):
    name: str
    description: Optional[str]
    lead_id: Optional[str]
