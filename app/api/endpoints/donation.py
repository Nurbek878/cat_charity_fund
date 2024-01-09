from fastapi import APIRouter, Depends
from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.user import User
from app.core.user import current_user, current_superuser

from app.schemas.donation import DonationAllDB, DonationCreate, DonationMyDB
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.investment import investment

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
    new_donation = await investment(new_donation, CharityProject, session)
    return new_donation


@router.get('/',
            response_model=list[DonationAllDB],
            response_model_exclude={'close_date', },
            dependencies=[Depends(current_superuser)])
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.get('/my',
            response_model=list[DonationMyDB],)
async def get_all_donations_user(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    donations = await donation_crud.get_by_user(user, session)
    return donations