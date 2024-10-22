from pymongo import MongoClient
from models.schemas import *
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

    def insert_post(self, post: PostRequest):
        post_data = {
            'usuario_id': post.user_id,
            'text': post.text,
            'images': post.images,
            'reacciones': [],
            'comentarios': []
        }

        res = self.db.posts.insert_one(post_data)
        post_data['_id'] = str(res.inserted_id)     # convertir el ObjectId a cadena
        return post_data


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
    


    def get_destinies(self):
        res = list(self.db.destinies.find())
        return self.serialize_object_ids(res)

    def register_destiny(self, destiny: DestinyRegister):
        destiny_data = {
            'user_id': destiny.user_id,
            'destiny_name' : destiny.destiny_name,
            'description' : destiny.description,
            'country' : destiny.country,
            'city' : destiny.city,
            'images': destiny.images,
            'likes': 0
        }

        res = self.db.destinies.insert_one(destiny_data)
        destiny_data['_id'] = str(res.inserted_id)     # convertir el ObjectId a cadena
        return destiny_data
    

    def get_wishlists(self):
        res = list(self.db.wishlists.find())
        return self.serialize_object_ids(res)

    def register_wishlist(self, wishlist: WishlistRegister):
        wishlist_data = {
            'user_id': wishlist.user_id,
            'list_name' : wishlist.list_name,
            'destinies' : wishlist.destinies,
            'followers' : []
        }

        res = self.db.wishlists.insert_one(wishlist_data)
        wishlist_data['_id'] = str(res.inserted_id)     # convertir el ObjectId a cadena
        return wishlist_data


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