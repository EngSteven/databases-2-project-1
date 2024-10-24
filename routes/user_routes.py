from fastapi import APIRouter, Depends
from models.schemas import *
from postgresql_data import Database  
from auth import * 

router = APIRouter()
db = Database()

@router.post("/users/user")
async def register_user(user: UserRegister):
    user_data = UserRegister(
        username=user.username,
        password=user.password,
        email=user.email
    )
    res = db.register_user(user_data)
    return res

@router.get("/users")
async def get_all_users():
    user = db.get_all_users()
    return user

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = db.get_user(user_id)
    return user


@router.put("/users/{user_id}/username")
async def update_username(user_id: int, request: UsernameRequest):
    res = db.update_username(user_id, request.username)
    return res

@router.put("/users/{user_id}/password")
async def update_password(user_id: int, request: PasswordRequest):
    res = db.update_password(user_id, request.password)
    return res

@router.delete("/users/{user_id}")
async def deactivate_user(user_id: int):
    res = db.deactivate_user(user_id)
    return res

@router.put("/users/{user_id}/reactivate")
async def reactivate_user(user_id: int):
    res = db.reactivate_user(user_id)
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


