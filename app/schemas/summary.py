from pydantic import BaseModel, HttpUrl
from datetime import datetime


class SummaryBase(BaseModel):
    url: HttpUrl


class SummaryCreate(SummaryBase):
    pass


class SummaryOut(SummaryBase):
    id: int
    summary_text: str
    created_at: datetime

    class Config:
        orm_mode = True
