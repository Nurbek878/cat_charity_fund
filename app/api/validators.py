from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charityproject_crud
from app.models.charityproject import CharityProject


async def check_name_duplicate(
        charityproject_name: str,
        session: AsyncSession,
) -> None:
    charityproject_id = await charityproject_crud.get_charityproject_id_by_name(charityproject_name, session)
    if charityproject_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )


async def check_charityproject_exists(
        charityproject_id: int,
        session: AsyncSession,
) -> CharityProject:
    charityproject = await charityproject_crud.get(
        charityproject_id, session
    )
    if charityproject is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charityproject