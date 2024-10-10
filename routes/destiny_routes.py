from fastapi import APIRouter
from models.schemas import DestinyRegister, DestinyTravelRegister
from postgresql_data import Database

router = APIRouter()
db = Database()

@router.post("/destiny")
async def register_destiny(destiny: DestinyRegister):
    destiny_data = DestinyRegister(
        name=destiny.name,
        description=destiny.description,
        location=destiny.location,
        url_image=destiny.url_image
    )
    res = db.register_destiny(destiny_data)
    return res

@router.post("/destiny/travel")
async def register_destiny_travel(destiny_travel: DestinyTravelRegister):
    destiny_travel_data = DestinyTravelRegister(
        travel_id=destiny_travel.travel_id,
        destiny_id=destiny_travel.destiny_id
    )
    res = db.register_destiny_travel(destiny_travel_data)
    return res
