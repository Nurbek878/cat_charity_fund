from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
        charityproject_name: str,
        session: AsyncSession,
) -> None:
    charityproject_id = await charityproject_crud.get_charityproject_id_by_name(charityproject_name, session)
    if charityproject_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден!'
        )
    return charityproject


async def check_invested_amount_is_not_null(
    charityproject_invested_amount: int,
):
    if charityproject_invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_fully_invested(
    charityproject_fully_invested: int,
):
    if charityproject_fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_full_amount_is_not_less(
    project_id: int, new_full_amount: int, session: AsyncSession
) -> None:
    project = await charityproject_crud.get(
        project_id, session
    )
    if new_full_amount and new_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Новая сумма не может быть меньше предыдущей',
        )
