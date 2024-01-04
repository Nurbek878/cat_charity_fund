from typing import Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charityproject import CharityProject
from app.schemas.charityproject import CharityProjectCreate, CharityProjectUpdate


async def create_charityproject(
        charityproject: CharityProjectCreate,
        session: AsyncSession) -> CharityProject:
    charityproject_data = charityproject.dict()

    db_charityproject = CharityProject(**charityproject_data)
    session.add(db_charityproject)
    await session.commit()
    await session.refresh(db_charityproject)
    return db_charityproject


async def get_charityproject_id_by_name(charityproject: str,
                                        session: AsyncSession
                                        ) -> Optional[int]:
    db_charityproject_id = await session.execute(
        select(CharityProject.id).where(
            CharityProject.name == charityproject))
    db_charityproject_id = db_charityproject_id.scalars().first()
    return db_charityproject_id


async def read_all_charityproj_from_db(
        session: AsyncSession,
) -> list[CharityProject]:
    db_charityproject = await session.execute(select(CharityProject))
    return db_charityproject.scalars().all()


async def get_charityproject_by_id(
        charityproject_id: int,
        session: AsyncSession,
) -> Optional[CharityProject]:
    db_charityproject = await session.execute(
        select(CharityProject).where(
            CharityProject.id == charityproject_id
        )
    )
    db_charityproject = db_charityproject.scalars().first()
    return db_charityproject


async def update_charityproject(
        db_charityproject: CharityProject,
        charityproject_in: CharityProjectUpdate,
        session: AsyncSession,
) -> CharityProject:
    obj_data = jsonable_encoder(db_charityproject)
    update_data = charityproject_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_charityproject, field, update_data[field])
    session.add(db_charityproject)
    await session.commit()
    await session.refresh(db_charityproject)
    return db_charityproject


async def delete_charityproject(
        db_charityproject: CharityProject,
        session: AsyncSession,
) -> CharityProject:
    await session.delete(db_charityproject)
    await session.commit()
    return db_charityproject
