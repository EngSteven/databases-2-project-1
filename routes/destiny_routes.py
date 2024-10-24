from fastapi import APIRouter, HTTPException
from models.schemas import *
from postgresql_data import Database
from mongo_data import DatabaseMongo  
from postgresql_data import Database  
from bson import ObjectId


#from auth import verify_token, oauth2_scheme  

router = APIRouter()
db_mongo = DatabaseMongo()
db_postgres = Database()

@router.get("/destinies")
async def get_destinies():
    res = db_mongo.get_destinies()
    print("All destinies: ", res)
    return {"All destinies": res}

@router.get("/destinies/destiny/{destiny_id}")
async def get_destiny(destiny_id: str):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    destiny_id = destiny_id.strip() # eliminar caracteres no deseados
    try:
        object_id = ObjectId(destiny_id)
    except:
        raise HTTPException(status_code=400, detail="El id del destino debe ser un ObjectId")
    res = db_mongo.get_destiny(object_id)
    
    return {"Destiny": res}

@router.get("/destinies/user/{user_id}")
async def get_user_destinies(user_id: int):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    res = db_mongo.get_user_destinies(user_id)
    return {"Destiny": res}

@router.post("/destinies/destiny/{user_id}")
async def register_destiny(user_id: int, destiny: DestinyRequest):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    # verificar si el id del usuarios ingresado existe en la base de datos 
    if db_postgres.check_user_exists(user_id):
        destiny_data = DestinyRequest(
            destiny_name = destiny.destiny_name,
            description = destiny.description,
            country = destiny.country,
            city = destiny.city,
            images = destiny.images 
        )
        res = db_mongo.register_destiny(user_id, destiny_data)
        return {"Destiny": res}
    
    return {"Error": "Usuario ingresado no existe"}

@router.delete("/destinies/destiny/{destiny_id}")
async def deactivate_destiny(destiny_id: str):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    destiny_id = destiny_id.strip() # eliminar caracteres no deseados
    try:
        object_id = ObjectId(destiny_id)
    except:
        raise HTTPException(status_code=400, detail="El id del destino debe ser un ObjectId")
    res = db_mongo.deactivate_destiny(object_id)
    return {"Destiny": res}
    
@router.put("/destinies/destiny/{destiny_id}/activate")
async def activate_destiny(destiny_id: str):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    destiny_id = destiny_id.strip() # eliminar caracteres no deseados
    try:
        object_id = ObjectId(destiny_id)
    except:
        raise HTTPException(status_code=400, detail="El id del destino debe ser un ObjectId")
    res = db_mongo.activate_destiny(object_id)
    return {"Destiny": res}


@router.put("/destinies/destiny/{user_id}/{destiny_id}")
async def update_destiny(user_id: int, destiny_id: str, destiny: DestinyRequest):
    # Verificar si el usuario existe en la base de datos PostgreSQL
    # verificar si el id del usuarios ingresado existe en la base de datos 
    if db_postgres.check_user_exists(user_id):
        destiny_data = DestinyRequest(
            destiny_name = destiny.destiny_name,
            description = destiny.description,
            country = destiny.country,
            city = destiny.city,
            images = destiny.images 
        )
        destiny_id = destiny_id.strip() # eliminar caracteres no deseados
        try:
            object_id = ObjectId(destiny_id)
        except:
            raise HTTPException(status_code=400, detail="El id del destino debe ser un ObjectId")
        
        res = db_mongo.update_destiny(object_id, destiny_data)
        return {"Destiny": res}
    
    return {"Error": "Usuario ingresado no existe"}