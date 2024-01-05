from fastapi import APIRouter, Depends
from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.models.user import User
from app.core.user import current_user

from app.schemas.donation import DonationCreate, DonationMyDB
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post('/',
             response_model=DonationMyDB,
             response_model_exclude_none=True)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> DonationMyDB:
    new_donation = await donation_crud.create(donation, session, user)
    return new_donation


@router.get('/', response_model=list[DonationMyDB])
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    donations = await donation_crud.get_multi(session)
    return donations
