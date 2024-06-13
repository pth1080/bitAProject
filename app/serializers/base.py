from typing import Optional

from pydantic import BaseModel, Field


class PaginateRequest(BaseModel):
    limit: Optional[int] = Field(10, alias='limit')
    offset: Optional[int] = Field(0, alias='offset')