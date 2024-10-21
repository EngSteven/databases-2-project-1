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

class Reaccion(Enum):
    me_gusta = "me gusta"
    me_encanta = "me encanta"
    me_enamora = "me enamora"
    me_asombra = "me asombra"
    me_entristece = "me entristece"
    me_enoja = "me enoja"

class Likes(BaseModel):
    react_id: int
    user_id: int
    reaccion: Reaccion

class Comentario(BaseModel):
    coment_id: int
    user_id: int
    coment_text: str
    reacciones: list

class Post(BaseModel):
    post_id: int
    user_id: int
    text: str
    images: list
    comentarios: list
    reacciones: list

class PostRequest(BaseModel):
    user_id: int
    text: str
    images: list

class ComentarioRequest(BaseModel):
    user_id: int
    coment_text: str

    
