from fastapi import APIRouter, Depends
from models.schemas import *
from mongo_data import DatabaseMongo  
from auth import * 

router = APIRouter()
db = DatabaseMongo()


@router.get("/posts")
async def obtener_post():
    return {"hola: mundo"}
    #res = db.obtener_posts(1)
    #return res

@router.post("/posts/post")
async def realizar_post(post: PostRequest):
    post_data = Post(
        post_id = 0,
        user_id = 1, #post.user_id
        text = post.text,
        images = post.images,
        comentarios = [],
        reacciones = []
    )
    res = db.insertar_post(post_data)
    return res