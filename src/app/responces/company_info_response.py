from typing import List, Optional

from pydantic import BaseModel

from app.models.holiday_model import Holiday


class CompanyInfoResponse(BaseModel):
    name: str
    description: Optional[str]
    lead_id: Optional[str]
    holidays: List[Holiday]
    document_ids: List[int]
