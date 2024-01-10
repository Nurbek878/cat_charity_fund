from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.api.validators import check_full_amount_is_not_less, check_fully_invested, check_invested_amount_is_not_null, check_name_duplicate, check_charityproject_exists
from app.models.donation import Donation

from app.schemas.charity_project import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
from app.services.investment import investment

router = APIRouter()


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)])
async def create_new_charityproject(
        charityproject: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    """Только для суперюзеров."""
    await check_name_duplicate(charityproject.name, session)
    new_charityproject = await charityproject_crud.create(charityproject, session)
    new_charityproject = await investment(
        new_charityproject, Donation, session
    )
    return new_charityproject


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charityproject(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charityproject = await check_charityproject_exists(
        project_id, session
    )
    await check_fully_invested(
        charityproject.fully_invested
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    await check_full_amount_is_not_less(project_id,
                                        obj_in.full_amount,
                                        session)
    charityproject = await investment(
        charityproject, Donation, session
    )
    charityproject = await charityproject_crud.update(
        charityproject, obj_in, session
    )
    return charityproject


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charityprojects(
        session: AsyncSession = Depends(get_async_session),
):
    all_charityprojects = await charityproject_crud.get_multi(session)
    return all_charityprojects


@router.delete(
    '/{project_id}',
    dependencies=[Depends(current_superuser)]
)
async def remove_charityproject(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charityproject = await check_charityproject_exists(
        project_id, session
    )
    await check_invested_amount_is_not_null(
        charityproject.invested_amount
    )
    charityproject = await charityproject_crud.remove(
        charityproject, session
    )
    return charityproject
