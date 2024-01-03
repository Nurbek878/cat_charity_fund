from sqlalchemy import Column, Text, Integer, ForeignKey

from app.models.basemodel import CharityDonationBase


class Donation(CharityDonationBase):

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)