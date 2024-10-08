from pydantic import BaseModel
from enum import Enum
from datetime import date 


class Roles(str, Enum):
    admin = "administrador"
    editor = "editor"
    lector = "lector"

class UserRegister(BaseModel):
    username: str
    password: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserId(BaseModel):
    id: int

class UserName(BaseModel):
    username: str

class User(BaseModel):
    id: int
    username: str
    password: str
    role: Roles

class Login(BaseModel):
    username: str
    password: str

class TravelRegister(BaseModel):
    user_id: int
    title: str
    description: str
    ini_date: date
    end_date: date 

class DestinyRegister(BaseModel):
    name: str
    description: str
    location: str
    url_image: str

class DestinyTravelRegister(BaseModel):
    travel_id: int
    destiny_id: int
    
