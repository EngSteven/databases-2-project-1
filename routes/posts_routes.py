from fastapi import APIRouter, Depends
from models.schemas import *
from mongo_data import DatabaseMongo  
from auth import * 
from bson import ObjectId

router = APIRouter()
db = DatabaseMongo()


@router.post("/{user_id}/posts/post")
async def insert_post(user_id: int, post: PostRequest): #Sirve
    post_data = PostRequest(
        text = post.text,
        images = post.images,
    )
    res = db.insert_post(user_id, post_data)
    print("Post: ", res)
    return {"Post ingresado": res}

@router.get("/{user_id}/posts")
async def get_posts(user_id: int):
    res = db.get_user_posts(user_id)    
    print("Posts:", res)
    return {"Posts recientes": res}

@router.get("/posts")
async def get_posts():
    res = db.get_all_posts()    
    print("Posts:", res)
    return {"Posts recientes": res}

@router.get("/{user_id}/posts/{post_id}")
async def get_post(post_id: str):
    res = db.get_user_post(ObjectId(post_id)) #Falta en mongo_data
    print("Post:", res)
    return {"Post": res}

@router.post("/{user_id}/posts/{post_id}/comment")
async def post_comment(user_id: int, post_id: str, comment: CommentRequest):
    post_data = CommentRequest(
        text = comment.coment_text
    )
    res = db.insert_comment(user_id, ObjectId(post_id), post_data)
    print("Comentario: ", res)
    return{"Comentario" : res}


#Este no sé si funciona
@router.post("/{user_id}/posts/{post_id}/react")
async def post_reaction(user_id: int, post_id: str, reaccion: LikesRequest):
    post_data = LikesRequest(
        reaction = reaccion.reaccion
    )
    res = db.insert_reaction(user_id, ObjectId(post_id), post_data)
    print("Reaccion: ", res)
    return{"Reaccion" : res}

@router.get("/{user_id}/posts/{post_id}/{comment_id}")
async def get_comment(comment_id: str):
    res = db.get_user_comment(ObjectId(comment_id))
    print("Comentario:", res)
    return {"Comentario": res}

@router.get("/{user_id}/posts/{post_id}/{reaction_id}")
async def get_reaction(reaction_id: str):
    res = db.get_user_reaction(ObjectId(reaction_id))
    print("Reaccion:", res)
    return {"Reaccion": res}

@router.put("/{user_id}/posts/{post_id}/update")
async def update_post(post_id: str, post: PostUpdateRequest):
    post_data = PostUpdateRequest(
        post_id = post_id,
        text = post.text,
        images = post.images,
    )
    res = db.update_post(post_data)
    print("Post: ", res)
    return {"Post actualizado": res}

@router.put("/{user_id}/posts/{post_id}/{comment_id}/update")
async def update_comment(comment_id: str, comment: CommentUpdateRequest):
    post_data = CommentUpdateRequest(
        comment_id = comment_id,
        coment_text = comment.coment_text
    )
    res = db.update_comment(post_data)
    print("Post: ", res)
    return {"Post actualizado": res}

@router.put("/{user_id}/posts/{post_id}/{reaction_id}/update")
async def update_reaction(reaction_id: str, reaccion: LikesUpdateRequest):
    post_data = LikesUpdateRequest(
        reaction_id = reaction_id, 
        reaccion = reaccion.reaccion
    )
    res = db.update_reaction(post_data)
    print("Post: ", res)
    return {"Post actualizado": res}

@router.delete("/{user_id}/posts/{post_id}/delete")
async def delete_post(post_id: str):
    db.delete_user_posts(ObjectId(post_id))
    return {"Posts borrado exitosamente"}

@router.delete("/{user_id}/posts/{post_id}/{comment_id}/delete")
async def delete_comment(comment_id: str): 
    db.delete__user_comment(ObjectId(comment_id))
    return {"Comentario eliminado exitosamente"}

@router.delete("/{user_id}/posts/{post_id}/{reaction_id}/delete")
async def delete_reaction(reaction_id: str):
    db.delete__user_reaction(ObjectId(reaction_id))
    return {"Reaccion eliminada correctamente"}

"""
TODO: 
    Flujo de interacción:
        1. Cuando el usuario ingresa lo que ve es un GET con los posts más recientes (Query para mostrar los post por ingreso) {user_id}/posts/
        2. Ingresar al post que quiera ver con {user_id}/posts/{post_id} y GET de ese post
        3. Si quiere comentar ese post utilizar el {user_id}/posts/{post_id}/comment con un POST
        4. Si quiere reaccionar a ese post utilizar el {user_id}/posts/{post_id}/react con un POST
        5. Si quiere ver el comentario utilizar el {user_id}/posts/{post_id}/{comment_id} con un GET
        6. Si quiere ver la reacción utilizar el {user_id}/posts/{post_id}/{reaction_id} con un GET
        7. Si quiere ingresar un nuevo post utilizar {user_id}/posts/post con un POST
        8. Si quiere modificar un post utilizar {user_id}/posts/{post_id}/update con un UPDATE
        9. Si quiere modificar un comentario utilizar {user_id}/posts/{post_id}/{comment_id}/update con un UPDATE
        10. Si quiere modificar una reacción utilizar {user_id}/posts/{post_id}/{reaction_id}/update con un UPDATE
        11. Si quiere eliminar un post utilizar {user_id}/posts/{post_id}/delete con un DELETE
        12. Si quiere eliminar un comentario utilizar {user_id}/posts/{post_id}/{comment_id}/delete con un DELETE
        13. Si quiere eliminar una reacción utilizar {user_id}/posts/{post_id}/{reaction_id}/delete con un DELETE
"""