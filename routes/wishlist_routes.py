from fastapi import APIRouter, Depends
from models.schemas import *
from postgresql_data import Database
from mongo_data import DatabaseMongo  
from postgresql_data import Database  


#from auth import verify_token, oauth2_scheme  

router = APIRouter()
db_mongo = DatabaseMongo()
db_postgres = Database()

@router.get("/wishlists")
async def get_wishlists():
    res = db_mongo.get_wishlists()
    print("All wishlists: ", res)
    return {"All wishlists": res}

@router.post("/wishlists/wishlist")
async def register_wishlist(wishlist: WishlistRegister):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    # verificar si el id del usuario ingresado existe en la base de datos 
    if db_postgres.check_user_exists(wishlist.user_id):
        wishlist_data = WishlistRegister(
            user_id = wishlist.user_id,
            list_name = wishlist.list_name,
            destinies = wishlist.destinies,
        )
        res = db_mongo.register_wishlist(wishlist_data)
        return {"wishlist": res}
    
    return {"Error": "Usuario ingresado no existe"}