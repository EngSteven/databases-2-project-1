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

@router.get("/wishlists/wishlist/{wishlist_id}")
async def get_wishlist(wishlist_id: str):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    wishlist_id = wishlist_id.strip() # eliminar caracteres no deseados
    try:
        object_id = ObjectId(wishlist_id)
    except:
        raise HTTPException(status_code=400, detail="El id del wishlist debe ser un ObjectId")
    res = db_mongo.get_wishlist(object_id)
    
    return {"wishlist": res}

@router.get("/wishlists/user/{user_id}")
async def get_user_wishlists(user_id: int):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    res = db_mongo.get_user_wishlists(user_id)
    return {"wishlist": res}

@router.post("/wishlists/wishlist/{user_id}")
async def register_wishlist(user_id: int, wishlist: WishlistRequest):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    # verificar si el id del usuario ingresado existe en la base de datos 
    if db_postgres.check_user_exists(user_id):
        wishlist_data = WishlistRequest(
            list_name = wishlist.list_name,
            destinies = wishlist.destinies,
        )
        res = db_mongo.register_wishlist(user_id, wishlist_data)
        return {"wishlist": res}
    
    return {"Error": "Usuario ingresado no existe"}

@router.delete("/wishlists/wishlist/{wishlist_id}")
async def deactivate_wishlist(wishlist_id: str):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    wishlist_id = wishlist_id.strip() # eliminar caracteres no deseados
    try:
        object_id = ObjectId(wishlist_id)
    except:
        raise HTTPException(status_code=400, detail="El id del wishlist debe ser un ObjectId")
    res = db_mongo.deactivate_wishlist(object_id)
    return {"wishlist": res}
    
@router.put("/wishlists/wishlist/{wishlist_id}/activate")
async def activate_wishlist(wishlist_id: str):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    wishlist_id = wishlist_id.strip() # eliminar caracteres no deseados
    try:
        object_id = ObjectId(wishlist_id)
    except:
        raise HTTPException(status_code=400, detail="El id del wishlist debe ser un ObjectId")
    res = db_mongo.activate_wishlist(object_id)
    return {"wishlist": res}


@router.put("/wishlists/wishlist/{user_id}/{wishlist_id}")
async def update_wishlist(user_id: int, wishlist_id: str, wishlist: WishlistRequest):
    # Verificar si el usuario existe en la base de datos PostgreSQL
    if db_postgres.check_user_exists(user_id):
        wishlist_data = WishlistRequest(
            list_name = wishlist.list_name,
            destinies = wishlist.destinies,
        )
        wishlist_id = wishlist_id.strip() # eliminar caracteres no deseados
        try:
            object_id = ObjectId(wishlist_id)
        except:
            raise HTTPException(status_code=400, detail="El id del wishlist debe ser un ObjectId")
        
        res = db_mongo.update_wishlist(object_id, wishlist_data)
        return {"wishlist": res}
    
    return {"Error": "Usuario ingresado no existe"}


@router.post("/wishlists/follow")
async def follow_wishlist(wishlist: WishlistFollow):
    # Verificar si el token es válido y el usuario está autenticado
    #username = verify_token(token)

    # verificar si el id del usuario ingresado existe en la base de datos 
    if db_postgres.check_user_exists(wishlist.user_id):
        wishlist_data = WishlistFollow(
            user_id = wishlist.user_id,
            wishlist_id = wishlist.wishlist_id
        )
        res = db_mongo.follow_wishlist(wishlist_data)
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