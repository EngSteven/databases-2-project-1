from fastapi import APIRouter, Depends
from models.schemas import *
from postgresql_data import Database  
from auth import * 

router = APIRouter()
db = Database()

@router.post("/user")
async def register_user(user: UserRegister):
    user_data = UserRegister(
        username=user.username,
        password=user.password,
        email=user.email
    )
    res = db.register_user(user_data)
    return res

@router.post("/login")
async def login(user: Login):
    user_data = Login(
        username=user.username,
        password=user.password
    )
    res = db.login(user_data)

    if res: 
        # Crear el token de autenticación
        token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=token_expires)

        # Almacenar el token en Redis con un tiempo de expiración
        redis_client.setex(user.username, ACCESS_TOKEN_EXPIRE_MINUTES * 60, access_token)
        
        return {"access_token": access_token, "user": user.username}

    return "Login fallido"
    

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)

    # eliminar el token del usuario en Redis para invalidar la sesión
    redis_client.delete(username)

    return {"message": "Logout exitoso"}


