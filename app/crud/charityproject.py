from typing import Optional
# from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase

from app.models.charityproject import CharityProject
# from app.schemas.charityproject import CharityProjectCreate, CharityProjectUpdate


class CRUDCharityProject(CRUDBase):

    async def get_charityproject_id_by_name(self,
                                            charityproject_name: str,
                                            session: AsyncSession
                                            ) -> Optional[int]:
        db_charityproject_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charityproject_name))
        db_charityproject_id = db_charityproject_id.scalars().first()
        return db_charityproject_id


charityproject_crud = CRUDCharityProject(CharityProject)
