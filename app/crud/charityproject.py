from app.core.db import AsyncSessionLocal
from app.models.charityproject import CharityProject
from app.schemas.charityproject import CharityProjectCreate


async def create_charityproject(
        charityproject: CharityProjectCreate
) -> CharityProject:
    charityproject_data = charityproject.dict()

    db_charityproject = CharityProject(**charityproject_data)

    async with AsyncSessionLocal() as session:
        session.add(db_charityproject)
        await session.commit()
        await session.refresh(db_charityproject)
    return db_charityproject
