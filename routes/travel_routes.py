from fastapi import APIRouter, HTTPException
from models.schemas import TravelRequest
from postgresql_data import Database
from mongo_data import DatabaseMongo  
from postgresql_data import Database  
from bson import ObjectId


#from auth import verify_token, oauth2_scheme  

router = APIRouter()
db_mongo = DatabaseMongo()
db_postgres = Database()

@router.get("/travels")
async def get_travels():
    res = db_mongo.get_travels()
    print("All travels: ", res)
    return {"All travels": res}

@router.get("/travels/travel/{travel_id}")
async def get_travel(travel_id: str):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    travel_id = travel_id.strip() # eliminar caracteres no deseados
    try:
        object_id = ObjectId(travel_id)
    except:
        raise HTTPException(status_code=400, detail="El id del travel debe ser un ObjectId")
    res = db_mongo.get_travel(object_id)
    
    return {"travel": res}

@router.get("/travels/user/{user_id}")
async def get_user_travels(user_id: int):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    res = db_mongo.get_user_travels(user_id)
    return {"travel": res}

@router.post("/travels/travel/{user_id}")
async def register_travel(user_id: int, travel: TravelRequest):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    # verificar si el id del usuario ingresado existe en la base de datos 
    if db_postgres.check_user_exists(user_id):
        travel_data = TravelRequest(
            trip_name = travel.trip_name,
            description = travel.description,
            places_visited = travel.places_visited,
        )
        res = db_mongo.register_travel(user_id, travel_data)
        return {"Travel": res}
    
    return {"Error": "Usuario ingresado no existe"}


@router.delete("/travels/travel/{travel_id}")
async def deactivate_travel(travel_id: str):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    travel_id = travel_id.strip() # eliminar caracteres no deseados
    try:
        object_id = ObjectId(travel_id)
    except:
        raise HTTPException(status_code=400, detail="El id del travel debe ser un ObjectId")
    res = db_mongo.deactivate_travel(object_id)
    return {"travel": res}
    
@router.put("/travels/travel/{travel_id}/activate")
async def activate_travel(travel_id: str):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    travel_id = travel_id.strip() # eliminar caracteres no deseados
    try:
        object_id = ObjectId(travel_id)
    except:
        raise HTTPException(status_code=400, detail="El id del travel debe ser un ObjectId")
    res = db_mongo.activate_travel(object_id)
    return {"travel": res}


@router.put("/travels/travel/{user_id}/{travel_id}")
async def update_travel(user_id: int, travel_id: str, travel: TravelRequest):
    # Verificar si el usuario existe en la base de datos PostgreSQL
    # verificar si el id del usuarios ingresado existe en la base de datos 
    if db_postgres.check_user_exists(user_id):
        travel_data = TravelRequest(
            trip_name = travel.trip_name,
            description = travel.description,
            places_visited = travel.places_visited,
        )
        travel_id = travel_id.strip() # eliminar caracteres no deseados
        try:
            object_id = ObjectId(travel_id)
        except:
            raise HTTPException(status_code=400, detail="El id del travel debe ser un ObjectId")
        
        res = db_mongo.update_travel(object_id, travel_data)
        return {"travel": res}
    
    return {"Error": "Usuario ingresado no existe"}