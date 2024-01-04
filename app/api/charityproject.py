from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session

from app.crud.charityproject import (create_charityproject, delete_charityproject,
                                     get_charityproject_id_by_name, read_all_charityproj_from_db,
                                     get_charityproject_by_id, update_charityproject)
from app.models.charityproject import CharityProject

from app.schemas.charityproject import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate

router = APIRouter(prefix='/charity_project',
                   tags=['charity_projects'])


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,)
async def create_new_charityproject(
        charityproject: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charityproject.name, session)
    new_charityproject = await create_charityproject(charityproject, session)
    return new_charityproject


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def partially_update_charityproject(
        charityproject_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charityproject = await get_charityproject_by_id(
        charityproject_id, session
    )
    charityproject = await check_charityproject_exists(
        charityproject_id, session
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    charityproject = await update_charityproject(
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
    all_charityprojects = await read_all_charityproj_from_db(session)
    return all_charityprojects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def remove_charityproject(
        charityproject_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charityproject = await check_charityproject_exists(
        charityproject_id, session
    )
    charityproject = await delete_charityproject(
        charityproject, session
    )
    return charityproject


async def check_name_duplicate(
        charityproject_name: str,
        session: AsyncSession,
) -> None:
    charityproject_id = await get_charityproject_id_by_name(charityproject_name, session)
    if charityproject_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )


async def check_charityproject_exists(
        charityproject_id: int,
        session: AsyncSession,
) -> CharityProject:
    charityproject = await get_charityproject_by_id(
        charityproject_id, session
    )
    if charityproject is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charityproject
