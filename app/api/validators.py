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
    if charityproject_invested_amount != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Удаление проектов, в которые уже внесены средства, запрещено.'
        )


async def check_full_amount_is_not_less(
    obj_full_amount: int, new_full_amount: int, session: AsyncSession
) -> None:
    if obj_full_amount < new_full_amount:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail='При редактировании проекта должно быть разрешено устанавливать требуемую сумму больше или равную внесённой',
        )
