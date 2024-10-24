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

@router.get("/wishlists")
async def get_wishlists():
    res = db_mongo.get_wishlists()
    print("All wishlists: ", res)
    return {"All wishlists": res}

@router.post("/wishlists/wishlist/{user_id}")
async def register_wishlist(user_id: int, wishlist: WishlistRequest):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    # verificar si el id del usuario ingresado existe en la base de datos 
    if db_postgres.check_user_exists(wishlist.user_id):
        wishlist_data = WishlistRequest(
            list_name = wishlist.list_name,
            destinies = wishlist.destinies,
        )
        res = db_mongo.register_wishlist(user_id, wishlist_data)
        return {"wishlist": res}
    
    return {"Error": "Usuario ingresado no existe"}

@router.post("/wishlists/follow/{user_id}/{wishlist_id}")
async def follow_wishlist(user_id: int, wishlist_id: int, wishlist: WishlistFollow):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    # verificar si el id del usuario ingresado existe en la base de datos 
    if db_postgres.check_user_exists(user_id):
        res = db_mongo.follow_wishlist(user_id, wishlist_id)
        return {"Resultado": res}
    
    return {"Error": "Usuario ingresado no existe"}

@router.delete("/wishlists/follow")
async def remove_follow_wishlist(wishlist: WishlistFollow):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    # verificar si el id del usuario ingresado existe en la base de datos 
    if db_postgres.check_user_exists(wishlist.user_id):
        wishlist_data = WishlistFollow(
            user_id = wishlist.user_id,
            wishlist_id = wishlist.wishlist_id
        )
        res = db_mongo.remove_follow_wishlist(wishlist_data)
        return {"Resultado": res}
    
    return {"Error": "Usuario ingresado no existe"}

@router.post("/wishlists/destiny")
async def add_destiny_to_wishlist(wishlist: WishlistDestiny):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    # verificar si el id del usuario ingresado existe en la base de datos 
    if db_postgres.check_user_exists(wishlist.user_id):
        wishlist_data = WishlistDestiny(
            user_id = wishlist.user_id,
            wishlist_id = wishlist.wishlist_id,
            destiny_id = wishlist.destiny_id
        )
        res = db_mongo.add_destiny_to_wishlist(wishlist_data)
        return {"Resultado": res}
    
    return {"Error": "Usuario ingresado no existe"}


@router.delete("/wishlists/destiny")
async def remove_destiny_from_wishlist(wishlist: WishlistDestiny):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    # verificar si el id del usuario ingresado existe en la base de datos 
    if db_postgres.check_user_exists(wishlist.user_id):
        wishlist_data = WishlistDestiny(
            user_id = wishlist.user_id,
            wishlist_id = wishlist.wishlist_id,
            destiny_id = wishlist.destiny_id
        )
        res = db_mongo.remove_destiny_from_wishlist(wishlist_data)
        return {"Resultado": res}
    
    return {"Error": "Usuario ingresado no existe"}