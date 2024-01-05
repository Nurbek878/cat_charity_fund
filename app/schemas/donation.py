from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationMyDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationAllDB(DonationMyDB):
    user_id: Optional[int]
    invested_amount: int = 0
    fully_invested: bool = False
    close_date: datetime = None
