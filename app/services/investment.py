from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.basemodel import CharityDonationBase


async def investment(
    obj_new: CharityDonationBase,
    obj_db: CharityDonationBase,
    session: AsyncSession
) -> CharityDonationBase:
    open_projects = await get_all_open_projects(obj_db, session)
    for project in open_projects:
        obj_new, project = await add_donations(
            obj_new, project
        )
        session.add(obj_new)
        session.add(project)
    await session.commit()
    await session.refresh(obj_new)
    return obj_new


async def get_all_open_projects(
    model_db: CharityDonationBase,
    session: AsyncSession
) -> list[CharityDonationBase]:
    source_db_all = await session.execute(select(model_db).where(
        model_db.fully_invested == 0).order_by(
            model_db.create_date)
    )
    source_db_all = source_db_all.scalars().all()
    return source_db_all


async def add_donations(
    obj_new: CharityDonationBase,
    obj_db: CharityDonationBase
) -> list[CharityDonationBase]:
    diff_new = obj_new.full_amount - obj_new.invested_amount
    diff_db = obj_db.full_amount - obj_db.invested_amount
    min_difference = min(diff_new, diff_db)
    if diff_new == diff_db:
        obj_new = await close_project(obj_new)
        obj_db = await close_project(obj_db)
    else:
        if diff_new > diff_db:
            obj_new.invested_amount += min_difference
            obj_db = await close_project(obj_db)
        else:
            obj_db.invested_amount += min_difference
            obj_new = await close_project(obj_new)
    return obj_new, obj_db


async def close_project(
    obj_db: CharityDonationBase
) -> CharityDonationBase:
    obj_db.invested_amount = obj_db.full_amount
    obj_db.fully_invested = True
    obj_db.close_date = datetime.now()
    return obj_db
