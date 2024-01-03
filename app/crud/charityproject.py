from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charityproject import CharityProject
from app.schemas.charityproject import CharityProjectCreate


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
