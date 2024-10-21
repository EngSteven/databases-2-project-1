from fastapi import APIRouter, Depends
from models.schemas import *
from mongo_data import DatabaseMongo  
from auth import * 
#from bson import ObjectId

router = APIRouter()
db = DatabaseMongo()

@router.get("/users/posts/{user_id}")
async def get_user_posts(user_id: int):
    res = db.get_user_posts(user_id)
    print("User posts: ", res)
    return {"user_posts": res} 

@router.post("/posts/post")
async def insert_post(post: PostRequest):
    post_data = PostRequest(
        user_id = post.user_id, 
        text = post.text,
        images = post.images,
    )
    res = db.insert_post(post_data)
    print("Post: ", res)
    return {"Post ingresado": res}
