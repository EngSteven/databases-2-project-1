from fastapi import APIRouter
from models.schemas import TravelRegister
from postgresql_data import Database

router = APIRouter()
db = Database()

@router.post("/travel")
async def register_travel(travel: TravelRegister):
    travel_data = TravelRegister(
        user_id=travel.user_id,
        title=travel.title,
        description=travel.description,
        ini_date=travel.ini_date,
        end_date=travel.end_date
    )
    res = db.register_travel(travel_data)
    return res
