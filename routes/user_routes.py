from fastapi import APIRouter
from models.schemas import UserRegister
from passlib.context import CryptContext
from postgresql_data import Database

router = APIRouter()
db = Database()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/user")
async def register_user(user: UserRegister):
    hashed_password = pwd_context.hash(user.password)
    user_data = UserRegister(
        username=user.username,
        password=hashed_password,
        email=user.email
    )
    res = db.register_user(user_data)
    return res

