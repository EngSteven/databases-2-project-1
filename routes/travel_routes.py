from fastapi import APIRouter, Depends
from models.schemas import TravelRegister
from postgresql_data import Database
from auth import verify_token, oauth2_scheme  

router = APIRouter()
db = Database()

@router.post("/travel")
async def register_travel(travel: TravelRegister, token: str = Depends(oauth2_scheme)):
    # Verificar si el token es válido y el usuario está autenticado
    username = verify_token(token)

    # Si el token es válido, proceder con el registro del viaje
    travel_data = TravelRegister(
        user_id=travel.user_id,
        title=travel.title,
        description=travel.description,
        ini_date=travel.ini_date,
        end_date=travel.end_date
    )
    res = db.register_travel(travel_data)
    return res
