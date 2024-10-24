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

class UsernameRequest(BaseModel):
    username: str

class PasswordRequest(BaseModel):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: int
    username: str
    password: str
    role: Roles

class Login(BaseModel):
    username: str
    password: str

class TravelRequest(BaseModel):
    trip_name: str
    description: str
    places_visited: list

class DestinyRegister(BaseModel):
    user_id: int
    destiny_name: str
    description: str
    country: str 
    city: str 
    images: list 

class DestinyRequest(BaseModel):
    destiny_name: str
    description: str
    country: str 
    city: str 
    images: list 



class WishlistRequest(BaseModel):
    list_name: str
    destinies: list

class WishlistFollow(BaseModel):
    user_id: int
    wishlist_id: str 

class WishlistDestiny(BaseModel):
    user_id: int
    wishlist_id: str 
    destiny_id: str

class Likes(BaseModel):
    react_id: str
    user_id: int
    reaccion: str
    active: bool

class LikesRequest(BaseModel):
    reaccion: str

class LikesUpdateRequest(BaseModel):
    reaction_id: str
    reaccion: str

class Comment(BaseModel):
    comment_id: str
    user_id: int
    coment_text: str
    reacciones: list
    active: bool

class Post(BaseModel):
    post_id: str
    user_id: int
    text: str
    images: list
    comentarios: list
    reacciones: list
    active: bool

class PostRequest(BaseModel):
    text: str
    images: list

class PostUpdateRequest(BaseModel):
    post_id: str
    text: str
    images: list

class CommentRequest(BaseModel):
    coment_text: str

class CommentUpdateRequest(BaseModel):
    comment_id: str
    coment_text: str

    