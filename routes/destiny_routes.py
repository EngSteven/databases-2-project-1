from fastapi import APIRouter, Depends
from models.schemas import *
from postgresql_data import Database
from mongo_data import DatabaseMongo  
from postgresql_data import Database  


#from auth import verify_token, oauth2_scheme  

router = APIRouter()
db_mongo = DatabaseMongo()
db_postgres = Database()

@router.get("/destinies")
async def get_destinies():
    res = db_mongo.get_destinies()
    print("All destinies: ", res)
    return {"All destinies": res}

@router.post("/destinies/destiny")
async def register_destiny(destiny: DestinyRegister):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    # verificar si el id del usuarios ingresado existe en la base de datos 
    if db_postgres.check_user_exists(destiny.user_id):
        destiny_data = DestinyRegister(
            user_id = destiny.user_id,
            destiny_name = destiny.destiny_name,
            description = destiny.description,
            country = destiny.country,
            city = destiny.city,
            images = destiny.images 
        )
        res = db_mongo.register_destiny(destiny_data)
        return {"Destiny": res}
    
    return {"Error": "Usuario ingresado no existe"}