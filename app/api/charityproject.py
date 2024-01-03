from fastapi import APIRouter

from app.crud.charityproject import create_charityproject
from app.schemas.charityproject import CharityProjectCreate

router = APIRouter()


@router.post('/charity_project/')
async def create_new_meeting_room(
        charityproject: CharityProjectCreate,
):
    new_room = await create_charityproject(charityproject)
    return new_room 