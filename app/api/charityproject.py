from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session

from app.crud.charityproject import create_charityproject, get_charityproject_id_by_name
from app.schemas.charityproject import CharityProjectCreate, CharityProjectDB

router = APIRouter()


@router.post('/charity_project/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,)
async def create_new_meeting_room(
        charityproject: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    room_id = await get_charityproject_id_by_name(charityproject.name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )
    new_charityproject = await create_charityproject(charityproject, session)
    return new_charityproject
