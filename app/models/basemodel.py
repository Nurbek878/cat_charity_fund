from datetime import datetime


from sqlalchemy import Column, Integer, Boolean, DateTime
from app.core.db import Base

class CharityDonationBase(Base):

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)