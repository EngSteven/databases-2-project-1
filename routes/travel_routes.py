from fastapi import APIRouter, Depends
from models.schemas import TravelRegister
from postgresql_data import Database
from mongo_data import DatabaseMongo  
from postgresql_data import Database  


#from auth import verify_token, oauth2_scheme  

router = APIRouter()
db_mongo = DatabaseMongo()
db_postgres = Database()

@router.get("/travels")
async def get_travels():
    res = db_mongo.get_travels()
    print("All travels: ", res)
    return {"All travels": res}

@router.post("/travels/travel")
async def register_travel(travel: TravelRegister):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    # verificar si el id del usuario ingresado existe en la base de datos 
    if db_postgres.check_user_exists(travel.user_id):
        travel_data = TravelRegister(
            user_id = travel.user_id,
            trip_name = travel.trip_name,
            description = travel.description,
            places_visited = travel.places_visited,
        )
        res = db_mongo.register_travel(travel_data)
        return {"Travel": res}
    
    return {"Error": "Usuario ingresado no existe"}