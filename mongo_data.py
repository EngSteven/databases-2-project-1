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

class DatabaseMongo:
    def __init__(self):
        client = MongoClient(
            host=config["host"],
            port=config["port"],
            username=config["username"],
            password=config["password"]
        )
        self.db = client[config["database"]]

    def close_connection(self):
        self.client.close()  

    def serialize_object_ids(self, docs):
        """Serializa una lista de documentos convirtiendo sus ObjectId a cadenas."""
        for doc in docs:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])  # convierte ObjectId a cadena
        return docs

    def get_user_posts(self, user_id):
        res = list(self.db.posts.find({"usuario_id": user_id}))
        return self.serialize_object_ids(res)

    def insert_post(self, user_id, post: PostRequest):
        post_data = {
            'usuario_id': user_id,
            'text': post.text,
            'images': post.images,
            'reacciones': [],
            'comentarios': []
        }

        res = self.db.posts.insert_one(post_data)
        post_data['_id'] = str(res.inserted_id)     # convertir el ObjectId a cadena
        return post_data

    def insert_comment(self, comment: CommentRequest):
        comment_data = {
            'user_id' : comment.user_id,
            'text' : comment.coment_text 
        }

    def get_travels(self):
        res = list(self.db.travels.find())
        return self.serialize_object_ids(res)

    def register_travel(self, travel: TravelRegister):
        travel_data = {
            'user_id': travel.user_id,
            'trip_name': travel.trip_name,
            'description': travel.description,
            'places_visited': travel.places_visited,
            'likes': 0
        }

        res = self.db.travels.insert_one(travel_data)
        travel_data['_id'] = str(res.inserted_id)     # convertir el ObjectId a cadena
        return travel_data
    


    """
    --------------------------------------------------------------------------------------------------------
    DESTINOS
    --------------------------------------------------------------------------------------------------------
    """

    def get_destinies(self):
        res = list(self.db.destinies.find())
        return self.serialize_object_ids(res)
    
    def get_destiny(self, destiny_id: ObjectId):
        res = list(self.db.destinies.find({"_id": destiny_id}))
        return self.serialize_object_ids(res)
    
    def get_user_destinies(self, user_id: int):
        res = list(self.db.destinies.find({"user_id": user_id}))
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
        # result = self.db.destinies.update_one(filter, update)
        
        result = self.db.destinies.update_one(
            { "_id": destiny_id },
            { "$set": { "destiny_name": destiny.destiny_name } }
        )

        # Comprobar si se actualizó alguna fila
        if result.modified_count > 0:
            return "Destino actualizado"
        else:
            return "No se encontró el destino ingresado"  # Indicar que no se encontró o no se modificó el destino


    def get_wishlists(self):
        res = list(self.db.wishlists.find())
        return self.serialize_object_ids(res)

    def register_wishlist(self, wishlist: WishlistRegister):
        wishlist_data = {
            'user_id': wishlist.user_id,
            'list_name' : wishlist.list_name,
            'destinies' : wishlist.destinies,
            'followers' : [],
            'num_followers': 0
        }

        res = self.db.wishlists.insert_one(wishlist_data)
        wishlist_data['_id'] = str(res.inserted_id)     # convertir el ObjectId a cadena
        return wishlist_data
    
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

        
        
    def remove_follow_wishlist(self, wishlist: WishlistFollow):
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

    # Añadir reacciones a los posts
    def add_reaction_to_post(self, post_id, react_id):
        res = self.db.posts.update_one(
            { "_id": ObjectId(post_id) },
            { "$addToSet": { "reacciones": react_id } }
        )
        if res.modified_count > 0:
            return "Reacción agregada al post con éxito."
        else:
            return "No se pudo agregar la reacción al post."
        

    # Quitar reacciones de los posts 
    def remove_reaction_from_post(self, post_id, react_id):
        res = self.db.posts.update_one(
            { "_id": ObjectId(post_id), "reacciones.react_id": react_id  },
            { "$set": { "reacciones.$.active": False } }
        )
        if res.modified_count > 0:
            return "Reacción removida del post con éxito."
        else:
            return "No se pudo remover la reacción del post."

    # Añadir comentarios a los posts
    def add_comment_to_post(self, post_id, comment: Comment):
        comment_data = comment.dict()
        comment_data['reacciones'] = []
        res = self.db.posts.update_one(
            { "_id": ObjectId(post_id) },
            { "$addToSet": { "comentarios": comment.coment_id } }
        )
        if res.modified_count > 0:
            return "Comentario agregado al post con éxito."
        else:
            return "No se pudo agregar el comentario al post."
    
    # Quitar comentarios de los posts
    def remove_comment_from_post(self, post_id, comment_id):
        res = self.db.posts.update_one(
            { "_id": ObjectId(post_id), "comentarios.coment_id": comment_id },
            { "$set": { "comentarios.$.active": False } }
        )
        if res.modified_count > 0:
            return "Comentario removido del post con éxito."
        else:
            return "No se pudo remover el comentario del post."

    # Añadir reacciones a los comentarios
    def add_reaction_to_comment(self, post_id, comment_id, react_id):
        res = self.db.posts.update_one(
            { "_id": ObjectId(post_id), "comentarios.coment_id": comment_id },
            { "$addToSet": { "comentarios.$.reacciones": react_id } }
        )
        if res.modified_count > 0:
            return "Reacción agregada al comentario con éxito."
        else:
            return "No se pudo agregar la reacción al comentario."
    
    # Quitar reacciones de los comentarios
    def remove_reaction_from_comment(self, post_id, comment_id, react_id):
        res = self.db.posts.update_one(
            { "_id": ObjectId(post_id), "comentarios.coment_id": comment_id },
            { "$pull": { "comentarios.$.reacciones": { "react_id": react_id } } }
        )
        if res.modified_count > 0:
            return "Reacción removida del comentario con éxito."
        else:
            return "No se pudo remover la reacción del comentario."


"""
class DatabaseMongo:
    def __init__(self):
        self.connection_string = 'mongodb://localhost:27017/'
        self.client = MongoClient(self.connection_string, username='root', password='root')
        self.db = self.client["PRY01"]
        self.posts_collection = self.db['posts']
        self.comentarios_collection = self.db['comentarios']
        self.reacciones_collection = self.db['reacciones']
    
    def insertar_post(self, post: Post):
        post = {
            'usuario_id' : post.user_id,
            'text' : post.text,
            'images' : post.images,
            'reacciones' : post.reacciones,
            'comentarios' : post.comentarios
        }

        resultado = self.posts_collection.insert_one(post)
        post.post_id = resultado.inserted_id

    def obtener_posts(self, user_id):
        res = self.posts_collection.find({"usuario_id": user_id})
        return res

    def insertar_comentario(self, comentario: Comentario, post_id):
    #     coment_id: int
    # user_id: int
    # coment_text: str
    # reacciones: list
        comentario = {
            'post_id' : post_id,
            'user_id' : comentario.coment_id,
            'text' : comentario.coment_text,
            'reacciones' : comentario.reacciones 
        }

        resultado = self.comentarios_collection.insert_one(comentario)

        self.posts_collection.update_one(
            {'_id' : post_id},
            {'$push' : {'comentarios' : comentario}}
        )

        comentario.coment_id = resultado.inserted_id

    def insertar_reaccion(self, reaccion: Likes, id):
    #     react_id: int
    # user_id: int
    # reaccion: Reaccion
        comentario = self.comentarios_collection.find_one({'_id' : id})
        post = self.posts_collection.find_one({'_id' : id})

        reaccion = {
            'reacted_id' : id,
            'user_id' : reaccion.user_id,
            'reaccion' : reaccion.reaccion
        }

        resultado = self.reacciones_collection.insert_one(reaccion)

        if comentario: 
            self.comentarios_collection.update_one(
                {'_id' : id},
                {'$push' : {'reacciones' : reaccion}}
            )
        elif post:
            self.posts_collection.update_one(
                {'_id' : id},
                {'$push' : {'reacciones' : reaccion}}
            )

"""