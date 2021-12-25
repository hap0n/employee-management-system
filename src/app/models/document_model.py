from typing import Optional

from pydantic import BaseModel


class Document(BaseModel):
    id: Optional[int] = None
    s3_bucket: str
