from pymongo import MongoClient
from models.schemas import *
from bson import ObjectId
import os

config = {
    "host": os.getenv("MONGO_HOST"), 
    "port": int(os.getenv("MONGO_PORT")), 
    "username": os.getenv("MONGO_USER"),
    "password": os.getenv("MONGO_PASSWORD"),
    "database": os.getenv("MONGO_DB")
}

reacciones = ["me gusta", "me encanta", "me emociona", "me asombra", "me entristece", "me enoja"]


class DatabaseMongo:
    def __init__(self):
        client = MongoClient(
            host=config["host"],
            port=config["port"],
            username=config["username"],
            password=config["password"]
        )
        self.db = client[config["database"]]
        self.reacciones = ["me gusta", "me encanta", "me enamora", "me asombra", "me entristece", "me enoja"]

    def close_connection(self):
        self.client.close()  

    def serialize_object_ids(self, docs):
        """Serializa una lista de documentos convirtiendo sus ObjectId a cadenas."""
        for doc in docs:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])  # convierte ObjectId a cadena
        return docs
    
    def verify_existing_ids(self, collection_name: str, ids: list):
        valid_ids = []
        
        for item_id in ids:
            # Convertir el ID a ObjectId
            try:
                object_id = ObjectId(item_id)
            except Exception as e:
                return {"Error": f"Formato de ObjectId incorrecto: {e}"}
            
            # Verificar si el ID existe y está activo
            exists = self.db[collection_name].find_one({"_id": object_id, "is_active": True})
            
            if not exists:
                return {"Error": f"El id {item_id} no existe o esta inactivo"}
            
            # Si el ID es válido, agregarlo a la lista
            valid_ids.append(object_id)
        
        return valid_ids
    
    def verify_existing_ids_posts(self, collection_name: str, ids: list):
        valid_ids = []
        
        for item_id in ids:
            # Convertir el ID a ObjectId
            try:
                object_id = ObjectId(item_id)
            except Exception as e:
                return {"Error": f"Formato de ObjectId incorrecto: {e}"}
            
            # Verificar si el ID existe y está activo
            exists = self.db[collection_name].find_one({"_id": object_id, "active": True})
            
            if not exists:
                return {"Error": f"El id {item_id} no existe o esta inactivo"}
            
            # Si el ID es válido, agregarlo a la lista
            valid_ids.append(object_id)
        
        return valid_ids

    """
    --------------------------------------------------------------------------------------------------------
    Viajes
    --------------------------------------------------------------------------------------------------------
    """

    def get_travels(self):
        res = list(self.db.travels.find({"is_active": True}))
        return self.serialize_object_ids(res)
    
    def get_travel(self, travel_id: ObjectId):
        res = list(self.db.travels.find({"_id": travel_id, "is_active": True}))
        return self.serialize_object_ids(res)
    
    def get_user_travels(self, user_id: int):
        res = list(self.db.travels.find({"user_id": user_id, "is_active": True}))
        return self.serialize_object_ids(res)
    
    def get_travel_destinies(self, travel_id: ObjectId):
        travel = self.db.travels.find_one({"_id": travel_id, "is_active": True})

        if travel:
            # Obtener los IDs de los destinos asociados en los viajes
            destiny_ids = travel.get("places_visited", [])

            # Asegurarse de que los destiny_ids sean ObjectId
            destiny_object_ids = []
            for destiny_id in destiny_ids:
                try:
                    destiny_object_ids.append(ObjectId(destiny_id))
                except Exception as e:
                    print(f"Error converting travel_id: {destiny_id} to ObjectId: {e}")
            
            # Buscar los viajes cuyos IDs están en destiny_object_ids y que estén activos
            destinies = list(self.db.destinies.find({"_id": {"$in": destiny_object_ids}, "is_active": True}))

            # Serializar los ObjectIds de los viajes
            return self.serialize_object_ids(destinies)
        
        return {"Error": "Viaje ingresado no existe"}

    def register_travel(self, user_id: int, travel: TravelRequest):
        # Verificar que todos los destinos ingresados existan en la base de datos de destinies
        valid_destinies = self.verify_existing_ids("destinies", travel.places_visited)
        
        if isinstance(valid_destinies, dict) and "Error" in valid_destinies:
            return valid_destinies  # Retornar error si hubo alguno


        travel_data = {
            'user_id': user_id,
            'trip_name': travel.trip_name,
            'description': travel.description,
            'places_visited': travel.places_visited,
            'is_active': True,
            'reacciones': [],
            'comentarios': []
        }

        res = self.db.travels.insert_one(travel_data)
        travel_data['_id'] = str(res.inserted_id)     # convertir el ObjectId a cadena
        return travel_data
    

    def deactivate_travel(self, travel_id: ObjectId):
        res = self.db.travels.update_one(
            { "_id": travel_id },
            { "$set": { "is_active": False } }
        )
        if res.modified_count > 0:
            return "Viaje desactivado con éxito."
        else:
            return "No se pudo desactivar el viaje."
        
    def activate_travel(self, travel_id: ObjectId):
        res = self.db.travels.update_one(
            { "_id": travel_id },
            { "$set": { "is_active": True } }
        )
        if res.modified_count > 0:
            return "Viaje activado con éxito."
        else:
            return "No se pudo activar el viaje."


    def update_travel(self, travel_id, travel: TravelUpdateRequest):
        updated_data = {
            'trip_name': travel.trip_name,
            'description': travel.description,
        }

        filter = {'_id': travel_id}
        update = {'$set': updated_data}
        
        # Realizar la actualización
        result = self.db.travels.update_one(filter, update)

        # Comprobar si se actualizó alguna fila
        if result.modified_count > 0:
            return "Viaje actualizado"
        else:
            return "No se encontró el viaje ingresado"  # Indicar que no se encontró o no se modificó el destino


    def add_destiny_to_travel(self, travel: TravelDestiny):
        # Verificar que el destino ingresado exista y esté activo
        destiny_exists = self.db.destinies.find_one({"_id": ObjectId(travel.destiny_id), "is_active": True})

        if not destiny_exists:
            return {"Error": "El destino ingresado no existe o está inactivo."}

        res = self.db.travels.update_one(
            { "_id": ObjectId(travel.travel_id), "user_id": travel.user_id},
            { "$addToSet": { "places_visited": travel.destiny_id } }
        )

        if res.modified_count > 0:
            return "Destino agregado al viaje con éxito." 
        else:
            return "No se encontró el viaje ingresado o el destino ya existe en el viaje."
    
    def remove_destiny_from_travel(self, travel: TravelDestiny):

        res = self.db.travels.update_one(
            { "_id": ObjectId(travel.travel_id), "user_id": travel.user_id},
            { "$pull": { "places_visited": travel.destiny_id } }
        )

        if res.modified_count > 0:
            return "Destino eliminado del viaje con éxito." 
        else:
            return "No se pudo encontrar el viaje o destino ingresado."


    """
    --------------------------------------------------------------------------------------------------------
    DESTINOS
    --------------------------------------------------------------------------------------------------------
    """

    def get_destinies(self):
        res = list(self.db.destinies.find({"is_active": True}))
        return self.serialize_object_ids(res)
    
    def get_destiny(self, destiny_id: ObjectId):
        res = list(self.db.destinies.find({"_id": destiny_id, "is_active": True}))
        return self.serialize_object_ids(res)
    
    def get_user_destinies(self, user_id: int):
        res = list(self.db.destinies.find({"user_id": user_id, "is_active": True}))
        return self.serialize_object_ids(res)

    def register_destiny(self, user_id: int, destiny: DestinyRequest):
        destiny_data = {
            'user_id': user_id,
            'destiny_name' : destiny.destiny_name,
            'description' : destiny.description,
            'country' : destiny.country,
            'city' : destiny.city,
            'images': destiny.images,
            'is_active': True,
            'reacciones': [],
            'comentarios': []
        }

        res = self.db.destinies.insert_one(destiny_data)
        destiny_data['_id'] = str(res.inserted_id)     # convertir el ObjectId a cadena
        return destiny_data
    
    def deactivate_destiny(self, destiny_id: ObjectId):
        res = self.db.destinies.update_one(
            { "_id": destiny_id },
            { "$set": { "is_active": False } }
        )
        if res.modified_count > 0:
            return "Destino desactivado con éxito."
        else:
            return "No se pudo desactivar el destino."
        
    def activate_destiny(self, destiny_id: ObjectId):
        res = self.db.destinies.update_one(
            { "_id": destiny_id },
            { "$set": { "is_active": True } }
        )
        if res.modified_count > 0:
            return "Destino activado con éxito."
        else:
            return "No se pudo activar el destino."


    def update_destiny(self, destiny_id, destiny: DestinyRequest):
        updated_data = {
            'destiny_name' : destiny.destiny_name,
            'description' : destiny.description,
            'country' : destiny.country,
            'city' : destiny.city,
            'images': destiny.images
        }

        # Filtro para identificar el destino que se va a actualizar
        filter = {'_id': destiny_id}
        
        # Actualización parcial utilizando $set para modificar solo los campos proporcionados
        update = {'$set': updated_data}
        
        # Realizar la actualización
        result = self.db.destinies.update_one(filter, update)

        # Comprobar si se actualizó alguna fila
        if result.modified_count > 0:
            return "Destino actualizado"
        else:
            return "No se encontró el destino ingresado"  # Indicar que no se encontró o no se modificó el destino


    """
    --------------------------------------------------------------------------------------------------------
    Lista de deseos
    --------------------------------------------------------------------------------------------------------
    """


    def get_wishlists(self):
        res = list(self.db.wishlists.find({"is_active": True}))
        return self.serialize_object_ids(res)
    
    def get_wishlist(self, wishlist_id: ObjectId):
        res = list(self.db.wishlists.find({"_id": wishlist_id, "is_active": True}))
        return self.serialize_object_ids(res)
    
    def get_user_wishlists(self, user_id: int):
        res = list(self.db.wishlists.find({"user_id": user_id, "is_active": True}))
        return self.serialize_object_ids(res)

    def get_wishlist_destinies(self, wishlist_id: ObjectId):
        wishlist = self.db.wishlists.find_one({"_id": wishlist_id, "is_active": True})

        if wishlist:
            # Obtener los IDs de los destinos asociados en la wishlist
            destiny_ids = wishlist.get("destinies", [])

            # Asegurarse de que los travel_ids sean ObjectId
            destiny_object_ids = []
            for destiny_id in destiny_ids:
                try:
                    destiny_object_ids.append(ObjectId(destiny_id))
                except Exception as e:
                    print(f"Error converting travel_id: {destiny_id} to ObjectId: {e}")
            
            # Buscar los viajes cuyos IDs están en travel_object_ids y que estén activos
            destinies = list(self.db.destinies.find({"_id": {"$in": destiny_object_ids}, "is_active": True}))

            # Serializar los ObjectIds de los viajes
            return self.serialize_object_ids(destinies)
        
        return {"Error": "Wishlist no existe"}

    def register_wishlist(self, user_id: int, wishlist: WishlistRequest):
        # Verificar que todos los destinos ingresados existan en la base de datos de destinies
        valid_destinies = self.verify_existing_ids("destinies", wishlist.destinies)
        
        if isinstance(valid_destinies, dict) and "Error" in valid_destinies:
            return valid_destinies  # Retornar error si hubo alguno

        wishlist_data = {
            'user_id': user_id,
            'list_name' : wishlist.list_name,
            'destinies' : wishlist.destinies,
            'followers' : [],
            'num_followers': 0,
            'is_active': True
        }

        res = self.db.wishlists.insert_one(wishlist_data)
        wishlist_data['_id'] = str(res.inserted_id)     # convertir el ObjectId a cadena
        return wishlist_data

    def deactivate_wishlist(self, wishlist_id: ObjectId):
        res = self.db.wishlists.update_one(
            { "_id": wishlist_id },
            { "$set": { "is_active": False } }
        )
        if res.modified_count > 0:
            return "Lista desactivada con éxito."
        else:
            return "No se pudo desactivar la lista."
        
    def activate_wishlist(self, wishlist_id: ObjectId):
        res = self.db.wishlists.update_one(
            { "_id": wishlist_id },
            { "$set": { "is_active": True } }
        )
        if res.modified_count > 0:
            return "Lista activada con éxito."
        else:
            return "No se pudo activar la lista."


    def update_wishlist(self, wishlist_id, wishlist: WishlistUpdateRequest):
        updated_data = {
            'list_name' : wishlist.list_name
        }

        # Filtro para identificar el destino que se va a actualizar
        filter = {'_id': wishlist_id}
        
        # Actualización parcial utilizando $set para modificar solo los campos proporcionados
        update = {'$set': updated_data}
        
        # Realizar la actualización
        result = self.db.wishlists.update_one(filter, update)

        # Comprobar si se actualizó alguna fila
        if result.modified_count > 0:
            return "Lista actualizada"
        else:
            return "No se encontró la lista ingresada"  # Indicar que no se encontró o no se modificó el destino

    def follow_wishlist(self, wishlist: WishlistFollow):
        wishlist_id = ObjectId(wishlist.wishlist_id)  # ID de la wishlist
        user_id = wishlist.user_id

        # verificar si el user_id está en la lista de followers
        is_follower = self.db.wishlists.find_one(
            { "_id": wishlist_id, "followers": user_id }
        )

        if not is_follower:
            # Si el user_id no está en la lista
            res = self.db.wishlists.update_one(
                { "_id": wishlist_id },
                {
                    "$addToSet": { "followers": user_id },   # Elimina el ID del usuario de la lista de followers
                    "$inc": { "num_followers": 1 }      # Decrementa el num_followers en 1
                }
            )

            if res.modified_count > 0:
                return "Follow realizado exitosamente."
            else:
                return "No se pudo actualizar la wishlist."
        else:
            return "El usuario ya estaba siguiendo la wishlist o la wishlist ingresada no existe."

        
    def remove_follow_wishlist(self, wishlist: WishlistRequest):
        wishlist_id = ObjectId(wishlist.wishlist_id)  # ID de la wishlist
        user_id = wishlist.user_id

        # verificar si el user_id está en la lista de followers
        is_follower = self.db.wishlists.find_one(
            { "_id": wishlist_id, "followers": user_id }
        )

        if is_follower:
            # Si el user_id está en la lista
            res = self.db.wishlists.update_one(
                { "_id": wishlist_id },
                {
                    "$pull": { "followers": user_id },   # Elimina el ID del usuario de la lista de followers
                    "$inc": { "num_followers": -1 }      # Decrementa el num_followers en 1
                }
            )

            if res.modified_count > 0:
                return "Follow removido exitosamente."
            else:
                return "No se pudo actualizar la wishlist."
        else:
            return "El usuario no sigue la wishlist o la wishlist ingresada no existe."
        

    
    # marcar destinos como objetivos propios
    def add_destiny_to_wishlist(self, wishlist: WishlistDestiny):
        # Verificar que el destino ingresado exista y esté activo
        destiny_exists = self.db.destinies.find_one({"_id": ObjectId(wishlist.destiny_id), "is_active": True})

        if not destiny_exists:
            return {"Error": "El destino ingresado no existe o está inactivo."}
        
        res = self.db.wishlists.update_one(
            { "_id": ObjectId(wishlist.wishlist_id), "user_id": wishlist.user_id},
            { "$addToSet": { "destinies": wishlist.destiny_id } }
        )

        if res.modified_count > 0:
            return "Destino agregado a la wishlist con éxito." 
        else:
            return "La wishlist ya contiene el destino o no se encontró la wishlist."
    

    # Eliminar destinos de la wishlist
    def remove_destiny_from_wishlist(self, wishlist: WishlistDestiny):
        res = self.db.wishlists.update_one(
            { "_id": ObjectId(wishlist.wishlist_id), "user_id": wishlist.user_id },
            { "$pull": { "destinies": wishlist.destiny_id } }  
        )

        if res.modified_count > 0:
            return "Destino eliminado de la wishlist con éxito."
        else:
            return "No se encontró el destino en la wishlist o no se encontró la wishlist."




    """
    --------------------------------------------------------------------------------------------------------
    POSTS
    --------------------------------------------------------------------------------------------------------
    """
    #TODO ver primero el active para mostrar solo las activas
    def get_user_posts(self, user_id):
        res = list(self.db.posts.find({"usuario_id": user_id, "active": True}).sort("visitas", -1))
        return self.serialize_object_ids(res)
    
    def get_all_posts(self):
        res = list(self.db.posts.find({"active" : True}).sort("visitas", -1))
        return self.serialize_object_ids(res)

    def insert_post(self, user_id, post: PostRequest):
        post_data = {
            'usuario_id': user_id,
            'text': post.text,
            'images': post.images,
            'reacciones': [],
            'comentarios': [],
            'visitas': 0,
            'active': True
        }

        res = self.db.posts.insert_one(post_data)
        post_data['_id'] = str(res.inserted_id)    
        return post_data

    def get_post_from_post(self, post_id):
        self.db.posts.update_one({"_id" : ObjectId(post_id), "$inc" : {"visitas" : 1}})
        res = list(self.db.posts.find(
             {"_id": ObjectId(post_id), "active" : True}
             ).sort("visitas", -1))
        # Si existe, regresa el post
        if res:
            return self.serialize_object_ids(res)
        else:
            return None
        
    def set_post(self, post_id: str, P_reaction: PostUpdateRequest):
        valid_ids = self.verify_existing_ids_posts("posts", [post_id])
        if isinstance(valid_ids, dict) and "Error" in valid_ids:
            return "Post no existe"
        
        res = self.db.posts.update_one(
            { "_id": ObjectId(post_id)},
            { "$set": { "text": P_reaction.text}}
        )
        if res.modified_count > 0:
            return "Reacción del post modificada con éxito."
        else:
            return "No se pudo modificar la reacción del post."
        
    def delete_post(self, post_id: str):
        valid_ids = self.verify_existing_ids_posts("posts", [post_id])
        if isinstance(valid_ids, dict) and "Error" in valid_ids:
            return "Post no existe"
        
        res = self.db.posts.update_one(
            { "_id": ObjectId(post_id)},
            { "$set": { "active": False }}
        )
        if res.modified_count > 0:
            return "Post borrado con éxito."
        else:
            return "No se pudo borrar el post."
    

    """
    --------------------------------------------------------------------------------------------------------
    COMMENTS
    --------------------------------------------------------------------------------------------------------
    """
    # Añadir comentarios a los posts
    def add_comment_to_post(self, user_id, post_id, comment: CommentRequest):
        valid_ids = self.verify_existing_ids_posts("posts", [post_id])
        if isinstance(valid_ids, dict) and "Error" in valid_ids:
            return valid_ids

        comment_data = {
            "usuario_id" : user_id,
            "comentario" : comment.coment_text,
            "reaccion" : [],
            "active" : True
        }
        comment_id = self.db.comentarios.insert_one(comment_data).inserted_id  
        res = self.db.posts.update_one(
            { "_id": ObjectId(post_id)},
            { "$push": { "comentarios": str(comment_id) } }
        )
        if res.modified_count > 0:
            return "Comentario agregado al post con éxito."
        else:
            return "No se pudo agregar el comentario al post."
    
    # Quitar comentarios de los posts
    def remove_comment_from_post(self, post_id, comment_id):
        valid_post = self.verify_existing_ids_posts("posts", [post_id])
        if isinstance(valid_post, dict) and "Error" in valid_post:
            return "Post no existe" 
        valid_reaction = self.verify_existing_ids_posts("comentarios", [comment_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Comentario no existe" 
        
        delete = self.db.comentarios.update_one(
            { "_id": ObjectId(comment_id)},
            { "$set": { "active": False }}
        )
        res = self.db.posts.update_one(
            { "_id": ObjectId(post_id)},
            { "$pull": { "comentarios": comment_id} }
        )
        if res.modified_count > 0 and delete.modified_count > 0:
            return "Comentario removido del post con éxito."
        else:
            return "No se pudo remover el comentario del post."
        
    def get_comment_from_post(self, comment_id):
        valid_reaction = self.verify_existing_ids_posts("comentarios", [comment_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Comentario no existe" 
        res = list(self.db.comentarios.find(
                {"_id": ObjectId(comment_id)}
                ))
        # Si existe, regresa la reaccion pedida
        return self.serialize_object_ids(res)
    
    def get_all_comments_from_post(self, post_id):
        valid_reaction = self.verify_existing_ids_posts("posts", [post_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Post no existe" 
        
        post = self.db.posts.find_one({"_id": ObjectId(post_id), "active": True})

        if post:
            # Obtener los IDs de los comentarios
            comment_ids = post.get("comentarios", [])
            
            # Obtener los comentarios correspondientes a los IDs
            comments = []
            if comment_ids:
                comments = list(self.db.comentarios.find({"_id": {"$in": [ObjectId(comment_id) for comment_id in comment_ids]}, "active": True}))
        
        # Si existe, regresa la reaccion pedida
        return self.serialize_object_ids(comments)
    
    def set_comment_from_post(self, comment_id, P_comment: CommentUpdateRequest):
        valid_reaction = self.verify_existing_ids_posts("comentarios", [comment_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Reaccion no existe" 
        res = self.db.comentarios.update_one(
            { "_id": ObjectId(comment_id)},
            { "$set": { "comentario": P_comment.coment_text } }
        )
        if res.modified_count > 0:
            return "Comentario del post modificado con éxito."
        else:
            return "No se pudo modificar el comentario del post."

    # Añadir comentarios a los posts
    def add_comment_to_destiny(self, user_id, destiny_id, destiny: DestinyRequest):
        valid_ids = self.verify_existing_ids("destinies", [destiny_id])
        if isinstance(valid_ids, dict) and "Error" in valid_ids:
            return valid_ids

        comment_data = {
            "usuario_id" : user_id,
            "comentario" : destiny.coment_text,
            "reaccion" : [],
            "active" : True
        }
        comment_id = self.db.comentarios.insert_one(comment_data).inserted_id  
        res = self.db.destinies.update_one(
            { "_id": ObjectId(destiny_id)},
            { "$push": { "comentarios": str(comment_id) } }
        )
        if res.modified_count > 0:
            return "Comentario agregado al destino con éxito."
        else:
            return "No se pudo agregar el comentario al destino."
    
    # Quitar comentarios de los posts
    def remove_comment_from_destiny(self, destiny_id, comment_id):
        valid_post = self.verify_existing_ids("destinies", [destiny_id])
        if isinstance(valid_post, dict) and "Error" in valid_post:
            return "Destino no existe" 
        valid_reaction = self.verify_existing_ids_posts("comentarios", [comment_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Comentario no existe" 
        
        delete = self.db.comentarios.update_one(
            { "_id": ObjectId(comment_id)},
            { "$set": { "active": False }}
        )
        res = self.db.destinies.update_one(
            { "_id": ObjectId(destiny_id)},
            { "$pull": { "comentarios": comment_id} }
        )
        if res.modified_count > 0 and delete.modified_count > 0:
            return "Comentario removido del destino con éxito."
        else:
            return "No se pudo remover el comentario del destino."
        
    def get_comment_from_destiny(self, comment_id):
        valid_reaction = self.verify_existing_ids_posts("comentarios", [comment_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Comentario no existe" 
        res = list(self.db.comentarios.find(
                {"_id": ObjectId(comment_id)}
                ))
        # Si existe, regresa la reaccion pedida
        return self.serialize_object_ids(res)
    
    def get_all_comments_from_destiny(self, destiny_id):
        valid_reaction = self.verify_existing_ids("destinies", [destiny_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Destino no existe" 
        
        post = self.db.destinies.find_one({"_id": ObjectId(destiny_id), "active": True})

        if post:
            # Obtener los IDs de los comentarios
            comment_ids = post.get("comentarios", [])
            
            # Obtener los comentarios correspondientes a los IDs
            comments = []
            if comment_ids:
                comments = list(self.db.comentarios.find({"_id": {"$in": [ObjectId(comment_id) for comment_id in comment_ids]}, "active": True}))
        
        # Si existe, regresa la reaccion pedida
        return self.serialize_object_ids(comments)
    
    def set_comment_from_destiny(self, comment_id, P_comment: CommentUpdateRequest):
        valid_reaction = self.verify_existing_ids_posts("comentarios", [comment_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Reaccion no existe" 
        res = self.db.comentarios.update_one(
            { "_id": ObjectId(comment_id)},
            { "$set": { "comentario": P_comment.coment_text } }
        )
        if res.modified_count > 0:
            return "Comentario del post modificado con éxito."
        else:
            return "No se pudo modificar el comentario del post."

    """
    --------------------------------------------------------------------------------------------------------
    REACTIONS
    --------------------------------------------------------------------------------------------------------
    """

    # Añadir reacciones a los posts
    def add_reaction_to_post(self, user_id, post_id, reaccion: LikesRequest):
        valid_ids = self.verify_existing_ids_posts("posts", [post_id])
        if isinstance(valid_ids, dict) and "Error" in valid_ids:
            return valid_ids
        
        reaction_data = {
            "usuario_id" : user_id,
            "reaccion" : reaccion.reaccion,
            "active" : True
        }
        react_id = self.db.reacciones.insert_one(reaction_data).inserted_id
        if reaccion.reaccion in self.reacciones:    
            res = self.db.posts.update_one(
                { "_id": ObjectId(post_id)},
                { "$push": { "reacciones": str(react_id) } }
            )
            if res.modified_count > 0:
                return "Reacción agregada al post con éxito."
            else:
                return "No se pudo agregar la reacción al post."
        return "Reacción no encontrada"
            

    # Quitar reacciones de los posts 
    def remove_reaction_from_post(self, post_id, react_id):
        valid_post = self.verify_existing_ids_posts("posts", [post_id])
        if isinstance(valid_post, dict) and "Error" in valid_post:
            return "Post no existe" 
        valid_reaction = self.verify_existing_ids_posts("reacciones", [react_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Reaccion no existe" 
        delete = self.db.reacciones.update_one(
            { "_id": ObjectId(react_id)},
            { "$set": { "active": False }}
        )
        res = self.db.posts.update_one(
            { "_id": ObjectId(post_id)},
            { "$pull": { "reacciones": react_id} }
        )
        if res.modified_count > 0 and delete.modified_count > 0:
            return "Reacción removida del post con éxito."
        else:
            return "No se pudo remover la reacción del post."

    def get_reaction_from_post(self, react_id):
        valid_reaction = self.verify_existing_ids_posts("reacciones", [react_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Reaccion no existe" 
        res = list(self.db.reacciones.find(
             {"_id": ObjectId(react_id)}
             ))
        # Si existe, regresa la reaccion pedida
        return self.serialize_object_ids(res)
    
    def get_all_reactions_from_post(self, post_id):
        valid_reaction = self.verify_existing_ids_posts("posts", [post_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Post no existe" 
        
        post = self.db.posts.find_one({"_id": ObjectId(post_id), "active": True})

        if post:
            # Obtener los IDs de los reacciones
            react_ids = post.get("reacciones", [])
            
            # Obtener los reacciones correspondientes a los IDs
            reactions = []
            if react_ids:
                reactions = list(self.db.reacciones.find({"_id": {"$in": [ObjectId(react_id) for react_id in react_ids]}, "active": True}))
        
        # Si existe, regresa la reaccion pedida
        return self.serialize_object_ids(reactions)
        
    def set_reaction_from_post(self, react_id, P_reaction: LikesUpdateRequest):
        valid_reaction = self.verify_existing_ids_posts("reacciones", [react_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Reaccion no existe" 
        if P_reaction.reaccion in reacciones:
            res = self.db.reacciones.update_one(
                { "_id": ObjectId(react_id)},
                { "$set": { "reaccion": P_reaction.reaccion } }
            )
            if res.modified_count > 0:
                return "Reacción del post modificada con éxito."
            else:
                return "No se pudo modificar la reacción del post."
        else:
            return "Reacción incorrecta"

    def add_reaction_to_destiny(self, user_id, destiny_id, reaccion: LikesRequest):
        valid_ids = self.verify_existing_ids("destinies", [destiny_id])
        if isinstance(valid_ids, dict) and "Error" in valid_ids:
            return valid_ids
        
        reaction_data = {
            "usuario_id" : user_id,
            "reaccion" : reaccion.reaccion,
            "active" : True
        }
        react_id = self.db.reacciones.insert_one(reaction_data).inserted_id
        if reaccion.reaccion in self.reacciones:    
            res = self.db.destinies.update_one(
                { "_id": ObjectId(destiny_id)},
                { "$push": { "reacciones": str(react_id) } }
            )
            if res.modified_count > 0:
                return "Reacción agregada al destino con éxito."
            else:
                return "No se pudo agregar la reacción al destino."
        return "Reacción no encontrada"
            

    # Quitar reacciones de los posts 
    def remove_reaction_from_destiny(self, destiny_id, react_id):
        valid_post = self.verify_existing_ids("destinies", [destiny_id])
        if isinstance(valid_post, dict) and "Error" in valid_post:
            return "Destino no existe" 
        valid_reaction = self.verify_existing_ids_posts("reacciones", [react_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Reaccion no existe" 
        delete = self.db.reacciones.update_one(
            { "_id": ObjectId(react_id)},
            { "$set": { "active": False }}
        )
        res = self.db.destinies.update_one(
            { "_id": ObjectId(destiny_id)},
            { "$pull": { "reacciones": react_id} }
        )
        if res.modified_count > 0 and delete.modified_count > 0:
            return "Reacción removida del destino con éxito."
        else:
            return "No se pudo remover la reacción del destino."

    def get_reaction_from_destiny(self, react_id):
        valid_reaction = self.verify_existing_ids_posts("reacciones", [react_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Reaccion no existe" 
        res = list(self.db.reacciones.find(
             {"_id": ObjectId(react_id)}
             ))
        # Si existe, regresa la reaccion pedida
        return self.serialize_object_ids(res)
    
    def get_all_reactions_from_destiny(self, destiny_id):
        valid_reaction = self.verify_existing_ids("destinies", [destiny_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Destino no existe" 
        
        post = self.db.destinies.find_one({"_id": ObjectId(destiny_id), "active": True})

        if post:
            # Obtener los IDs de los reacciones
            react_ids = post.get("reacciones", [])
            
            # Obtener los reacciones correspondientes a los IDs
            reactions = []
            if react_ids:
                reactions = list(self.db.reacciones.find({"_id": {"$in": [ObjectId(react_id) for react_id in react_ids]}, "active": True}))
        
        # Si existe, regresa la reaccion pedida
        return self.serialize_object_ids(reactions)
        
    def set_reaction_from_destiny(self, react_id, P_reaction: LikesUpdateRequest):
        valid_reaction = self.verify_existing_ids_posts("reacciones", [react_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Reaccion no existe" 
        if P_reaction.reaccion in reacciones:
            res = self.db.reacciones.update_one(
                { "_id": ObjectId(react_id)},
                { "$set": { "reaccion": P_reaction.reaccion } }
            )
            if res.modified_count > 0:
                return "Reacción del destino modificada con éxito."
            else:
                return "No se pudo modificar la reacción del destino."
        else:
            return "Reacción incorrecta"
            

    def add_reaction_to_comment(self, user_id, comment_id, reaccion: LikesRequest):
        valid_ids = self.verify_existing_ids_posts("comentarios", [comment_id])
        if isinstance(valid_ids, dict) and "Error" in valid_ids:
            return valid_ids
        
        reaction_data = {
            "usuario_id" : user_id,
            "reaccion" : reaccion.reaccion,
            "active" : True
        }
        react_id = self.db.reacciones.insert_one(reaction_data).inserted_id
        if reaccion.reaccion in self.reacciones:    
            res = self.db.comentarios.update_one(
                { "_id": ObjectId(comment_id)},
                { "$push": { "reacciones": str(react_id) } }
            )
            if res.modified_count > 0:
                return "Reacción agregada al comentario con éxito."
            else:
                return "No se pudo agregar la reacción al comentario."
        return "Reacción no encontrada"
            

    # Quitar reacciones de los posts 
    def remove_reaction_from_comment(self, comment_id, react_id):
        valid_post = self.verify_existing_ids_posts("comentarios", [comment_id])
        if isinstance(valid_post, dict) and "Error" in valid_post:
            return "Destino no existe" 
        valid_reaction = self.verify_existing_ids_posts("reacciones", [react_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Reaccion no existe" 
        delete = self.db.reacciones.update_one(
            { "_id": ObjectId(react_id)},
            { "$set": { "active": False }}
        )
        res = self.db.comentarios.update_one(
            { "_id": ObjectId(comment_id)},
            { "$pull": { "reacciones": react_id} }
        )
        if res.modified_count > 0 and delete.modified_count > 0:
            return "Reacción removida del comentario con éxito."
        else:
            return "No se pudo remover la reacción del comentario."

    def get_reaction_from_comment(self, react_id):
        valid_reaction = self.verify_existing_ids_posts("reacciones", [react_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Reaccion no existe" 
        res = list(self.db.reacciones.find(
             {"_id": ObjectId(react_id)}
             ))
        # Si existe, regresa la reaccion pedida
        return self.serialize_object_ids(res)
    
    def get_all_reactions_from_comment(self, comment_id):
        valid_reaction = self.verify_existing_ids("comentarios", [comment_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Comentario no existe" 
        
        post = self.db.destinies.find_one({"_id": ObjectId(comment_id), "active": True})

        if post:
            # Obtener los IDs de los reacciones
            react_ids = post.get("reacciones", [])
            
            # Obtener los reacciones correspondientes a los IDs
            reactions = []
            if react_ids:
                reactions = list(self.db.reacciones.find({"_id": {"$in": [ObjectId(react_id) for react_id in react_ids]}, "active": True}))
        
        # Si existe, regresa la reaccion pedida
        return self.serialize_object_ids(reactions)
        
    def set_reaction_from_comment(self, react_id, P_reaction: LikesUpdateRequest):
        valid_reaction = self.verify_existing_ids_posts("reacciones", [react_id])
        if isinstance(valid_reaction, dict) and "Error" in valid_reaction:
            return "Reaccion no existe" 
        if P_reaction.reaccion in reacciones:
            res = self.db.reacciones.update_one(
                { "_id": ObjectId(react_id)},
                { "$set": { "reaccion": P_reaction.reaccion } }
            )
            if res.modified_count > 0:
                return "Reacción del destino modificada con éxito."
            else:
                return "No se pudo modificar la reacción del destino."
        else:
            return "Reacción incorrecta"

