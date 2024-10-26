import unittest
from fastapi.testclient import TestClient
from postgresql_data import Database  

from app import app 

client = TestClient(app)
db = Database()


print("\n Ejecutando pruebas unitarias \n")

class TestAPI(unittest.TestCase):   

    @classmethod
    def setUpClass(cls):
        cls.user_token = None
        # Crear un usuario temporal para pruebas
        """
        cls.user_data = {
            "username": "testuser4",
            "password": "testpassword",
            "email": "testuser@example.com4"
        }
        response = client.post("/users/user", json=cls.user_data)
        assert response.status_code == 200, "Error al crear el usuario para pruebas"
        cls.user_id = response.json()["id"]  # Obtener el ID del usuario creado
        """
        cls.user_id = 1

        # Crear un destino temporal para pruebas
        cls.destiny_data = {
            "destiny_name": "Test Destiny",
            "description": "Test description",
            "country": "Test Country",
            "city": "Test City",
            "images": ["http://example.com/image1.jpg", "http://example.com/image2.jpg"]
        }
        response = client.post(f"/destinies/destiny/{cls.user_id}", json=cls.destiny_data)
        assert response.status_code == 200, "Error al crear el destino para pruebas"
        cls.destiny_id = response.json()["Destiny"]["_id"]  # Obtener el ID del destino creado

        # crear un travel de prueba
        cls.travel_data = {
            "trip_name": "Test Trip",
            "description": "Test trip description",
            "places_visited": [cls.destiny_id]
        }
        response = client.post(f"/travels/travel/{cls.user_id}", json=cls.travel_data)
        assert response.status_code == 200, "Error al crear el travel para pruebas"
        cls.travel_id = response.json()["Travel"]["_id"]

        # crear una wishlist de prueba
        cls.wishlist_data = {
            "list_name": "Test Wishlist",
            "destinies": [cls.destiny_id]
        }
        response = client.post(f"/wishlists/wishlist/{cls.user_id}", json=cls.wishlist_data)
        assert response.status_code == 200, "Error al crear el wishlist para pruebas"
        cls.wishlist_id = response.json()["wishlist"]["_id"]

        # crear un post de prueba
        cls.post_data = {
            "text": "Test post content",
            "images": ["http://example.com/image1.jpg", "http://example.com/image2.jpg"]
        }
        # Crear un post inicial
        response = client.post(f"/{cls.user_id}/posts/post", json=cls.post_data)
        assert response.status_code == 200, "Error al crear el post para pruebas"
        cls.post_id = response.json()["Post ingresado"]["_id"]  # Obtener el ID del post creado

        # Crear un comentario de prueba
        cls.comment_data = {
            "coment_text": "This is a test comment"
        }
        response = client.post(f"/{cls.user_id}/posts/{cls.post_id}/comment", json=cls.comment_data)
        assert response.status_code == 200, "Error al crear el comentario para pruebas"
        cls.comment_id = response.json()["Comentario"]


        # Crear una reacción de prueba y obtener el ID como str directamente
        cls.reaction_data = {
            "reaccion": "like"
        }
        response = client.post(f"/{cls.user_id}/posts/{cls.post_id}/react", json=cls.reaction_data)
        assert response.status_code == 200, "Error al crear la reacción para pruebas"
        cls.reaction_id = response.json()["Reaccion"]  # Obtener el ID de la reacción como str



    @classmethod
    def tearDownClass(cls):
        client.delete(f"/users/{cls.user_id}")
        client.delete(f"/destinies/destiny/{cls.destiny_id}")
        client.delete(f"/travels/travel/{cls.travel_id}")
        client.delete(f"/wishlists/wishlist/{cls.wishlist_id}")
        client.delete(f"/{cls.user_id}/posts/{cls.post_id}/delete")
        client.delete(f"/{cls.user_id}/posts/{cls.post_id}/comment/{cls.comment_id}/delete")


    """
    ------------------------------------------------------------------------------------------------------
    PRUEBAS PARA USUARIOS
    ------------------------------------------------------------------------------------------------------
    """

    def test_check_user_exist(self):
        response = client.post(f"/users/exist/{self.user_id}")
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        user_data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com"
        }
        response = client.post("/users/user", json=user_data)
        self.assertEqual(response.status_code, 200)

    def test_get_all_users(self):
        response = client.get("/users")
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        response = client.get(f"/users/{self.user_id}")
        self.assertEqual(response.status_code, 200)

    def test_deactivate_user(self):
        response = client.delete(f"/users/{self.user_id}")
        self.assertEqual(response.status_code, 200)

    def test_reactivate_user(self):
        client.delete(f"/users/{self.user_id}")  # Desactivar primero
        response = client.put(f"/users/{self.user_id}/reactivate")
        self.assertEqual(response.status_code, 200)

    def test_update_username(self):
        updated_username = {"username": "updated_user"}
        response = client.put(f"/users/{self.user_id}/username", json=updated_username)
        self.assertEqual(response.status_code, 200)

    def test_update_password(self):
        updated_password = {"password": "newpassword"}
        response = client.put(f"/users/{self.user_id}/password", json=updated_password)
        self.assertEqual(response.status_code, 200)

    
    def test_login(self):
        login = {
            "username": "nombre_usuario",
            "password": "contraseña_segura"
        }
        response = client.post("/login", json=login)
        self.assertEqual(response.status_code, 200, "Se esperaba un inicio de sesión exitoso.")
        
        response_data = response.json()
        self.assertIn("access_token", response_data, "Se esperaba recibir un 'access_token'.")
        # guardar el token para usarlo en otras pruebas
        TestAPI.user_token = response_data["access_token"]

    def test_logout(self):                   
        headers = {
            "Authorization": f"Bearer {TestAPI.user_token}"
        }

        response = client.post("/logout", headers=headers)

        self.assertEqual(response.status_code, 200, "Se esperaba un logout exitoso.")
    
    
    """
    ------------------------------------------------------------------------------------------------------
    PRUEBAS PARA DESTINOS
    ------------------------------------------------------------------------------------------------------
    """
        
    def test_get_destinies(self):
        response = client.get("/destinies")
        self.assertEqual(response.status_code, 200)
        self.assertIn("All destinies", response.json())

    def test_get_destiny(self):
        print("destiny id de prueba: ", self.destiny_id, "user id de prueba", self.user_id)
        response = client.get(f"/destinies/destiny/{self.destiny_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Destiny", response.json())
    
    def test_get_user_destinies(self):
        response = client.get(f"/destinies/user/{self.user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Destiny", response.json())

    def test_deactivate_destiny(self):
        response = client.delete(f"/destinies/destiny/{self.destiny_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Destiny", response.json())
        # Reactivar para mantener el destino para otros tests
        client.put(f"/destinies/destiny/{self.destiny_id}/activate")

    def test_activate_destiny(self):
        client.delete(f"/destinies/destiny/{self.destiny_id}")  # Desactivar primero
        response = client.put(f"/destinies/destiny/{self.destiny_id}/activate")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Destiny", response.json())

    def test_update_destiny(self):
        updated_destiny_data = {
            "destiny_name": "Updated Destiny Name",
            "description": "Updated description",
            "country": "Updated Country",
            "city": "Updated City",
            "images": ["http://example.com/updated_image1.jpg"]
        }
        response = client.put(f"/destinies/destiny/{self.user_id}/{self.destiny_id}", json=updated_destiny_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Destiny", response.json())

    """
    ------------------------------------------------------------------------------------------------------
    PRUEBAS DE ERROR PARA DESTINOS 
    ------------------------------------------------------------------------------------------------------
    """

    def test_get_nonexistent_destiny(self):
        response = client.get("/destinies/destiny/nonexistent_id")
        self.assertEqual(response.status_code, 400)  
        self.assertIn("detail", response.json())

    def test_delete_nonexistent_destiny(self):
        response = client.delete("/destinies/destiny/nonexistent_id")
        self.assertEqual(response.status_code, 400)  
        self.assertIn("detail", response.json())

    def test_create_destiny_invalid_data(self):
        invalid_destiny_data = {
            "description": "Missing name and other fields"
        }
        response = client.post(f"/destinies/destiny/{self.user_id}", json=invalid_destiny_data)
        self.assertEqual(response.status_code, 422)  
        self.assertIn("detail", response.json())  

    def test_update_destiny_with_invalid_user(self):
        updated_destiny_data = {
            "destiny_name": "Attempted Update",
            "description": "Attempted update with invalid user",
            "country": "Invalid Country",
            "city": "Invalid City",
            "images": ["http://example.com/invalid_image.jpg"]
        }
        response = client.put(f"/destinies/destiny/invalid_user_id/{self.destiny_id}", json=updated_destiny_data)
        self.assertEqual(response.status_code, 422)  
        self.assertIn("detail", response.json())

    """
    ------------------------------------------------------------------------------------------------------
    PRUEBAS PARA COMENTARIOS DE DESTINOS
    ------------------------------------------------------------------------------------------------------
    """

    
    def test_get_comment_destiny(self):
        response = client.get(f"/{self.user_id}/destinies/{self.destiny_id}/comment/{self.comment_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Comentario", response.json())

    def test_get_all_comments_destiny(self):
        response = client.get(f"/{self.user_id}/destinies/{self.destiny_id}/comments/all")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Comentarios", response.json())

    def test_update_comment_destiny(self):
        updated_data = {
            "coment_text": "This is an updated test comment"
        }
        response = client.put(f"/{self.user_id}/destinies/{self.destiny_id}/comment/{self.comment_id}/update", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Destiny actualizado", response.json())
    

    """
    ------------------------------------------------------------------------------------------------------
    PRUEBAS PARA REACCIONES DE DESTINOS
    ------------------------------------------------------------------------------------------------------
    """
    
    def test_get_reaction_destiny(self):
        response = client.get(f"/{self.user_id}/destinies/{self.destiny_id}/reaction/{self.reaction_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Reaccion", response.json())

    def test_get_all_reactions_destiny(self):
        response = client.get(f"/{self.user_id}/destinies/{self.destiny_id}/reactions/all")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Reacciones", response.json())

    def test_update_reaction_destiny(self):
        updated_data = {
            "reaccion": "love"
        }
        response = client.put(f"/{self.user_id}/destinies/{self.destiny_id}/reaction/{self.reaction_id}/update", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Reaccion actualizada", response.json())

    

    """
    ------------------------------------------------------------------------------------------------------
    PRUEBAS PARA VIAJES
    ------------------------------------------------------------------------------------------------------
    """

    def test_get_travels(self):
        response = client.get("/travels")
        self.assertEqual(response.status_code, 200)
        self.assertIn("All travels", response.json())

    def test_get_travel(self):
        response = client.get(f"/travels/travel/{self.travel_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("travel", response.json())

    def test_get_user_travels(self):
        response = client.get(f"/travels/user/{self.user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("travel", response.json())

    def test_deactivate_travel(self):
        response = client.delete(f"/travels/travel/{self.travel_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("travel", response.json())
        client.put(f"/travels/travel/{self.travel_id}/activate")

    def test_activate_travel(self):
        client.delete(f"/travels/travel/{self.travel_id}")
        response = client.put(f"/travels/travel/{self.travel_id}/activate")
        self.assertEqual(response.status_code, 200)
        self.assertIn("travel", response.json())

    def test_update_travel(self):
        updated_travel_data = {
            "trip_name": "Updated Trip",
            "description": "Updated description"
        }
        response = client.put(f"/travels/travel/{self.user_id}/{self.travel_id}", json=updated_travel_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("travel", response.json())

    def test_get_travel_destinies(self):
        response = client.get(f"/travels/destinies/{self.travel_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Destinies", response.json())

    def test_add_destiny_to_travel(self):
        destiny_data = {
            "user_id": self.user_id,
            "travel_id": self.travel_id,
            "destiny_id": self.destiny_id
        }
        response = client.post("/travels/destiny", json=destiny_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Resultado", response.json())



    """
    ------------------------------------------------------------------------------------------------------
    PRUEBAS DE ERROR PARA VIAJES
    ------------------------------------------------------------------------------------------------------
    """


    def test_get_nonexistent_travel(self):
        response = client.get("/travels/travel/nonexistent_id")
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json())

    def test_delete_nonexistent_travel(self):
        response = client.delete("/travels/travel/nonexistent_id")
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json())

    def test_create_travel_invalid_data(self):
        invalid_travel_data = {
            "description": "Missing trip name"
        }
        response = client.post(f"/travels/travel/{self.user_id}", json=invalid_travel_data)
        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.json())

    
    """
    ------------------------------------------------------------------------------------------------------
    PRUEBAS PARA LISTA DE DESEOS
    ------------------------------------------------------------------------------------------------------
    """

    def test_get_wishlists(self):
        response = client.get("/wishlists")
        self.assertEqual(response.status_code, 200)
        self.assertIn("All wishlists", response.json())

    def test_get_wishlist(self):
        response = client.get(f"/wishlists/wishlist/{self.wishlist_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("wishlist", response.json())

    def test_get_user_wishlists(self):
        response = client.get(f"/wishlists/user/{self.user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("wishlist", response.json())

    def test_get_wishlist_destinies(self):
        response = client.get(f"/wishlists/destinies/{self.wishlist_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Destinies", response.json())

    def test_deactivate_wishlist(self):
        response = client.delete(f"/wishlists/wishlist/{self.wishlist_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("wishlist", response.json())

    def test_activate_wishlist(self):
        response = client.put(f"/wishlists/wishlist/{self.wishlist_id}/activate")
        self.assertEqual(response.status_code, 200)
        self.assertIn("wishlist", response.json())

    def test_update_wishlist(self):
        update_data = {"list_name": "Updated Wishlist"}
        response = client.put(f"/wishlists/wishlist/{self.user_id}/{self.wishlist_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("wishlist", response.json())

    def test_follow_wishlist(self):
        follow_data = {"user_id": self.user_id, "wishlist_id": self.wishlist_id}
        response = client.post("/wishlists/follow", json=follow_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Resultado", response.json())

    def test_add_destiny_to_wishlist(self):
        destiny_data = {"user_id": self.user_id, "wishlist_id": self.wishlist_id, "destiny_id": self.destiny_id}
        response = client.post("/wishlists/destiny", json=destiny_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Resultado", response.json())


    """
    ------------------------------------------------------------------------------------------------------
    PRUEBAS DE ERROR PARA LISTA DE DESEOS
    ------------------------------------------------------------------------------------------------------
    """


    def test_register_wishlist_invalid_user_id(self):
        invalid_user_id = -1  # Suponiendo que este ID no existe
        wishlist_data = {
            "list_name": "Nonexistent User Wishlist",
            "destinies": []
        }
        response = client.post(f"/wishlists/wishlist/{invalid_user_id}", json=wishlist_data)
        self.assertEqual(response.status_code, 200)  # Dependiendo de la configuración, podría ser 400 o 404
        self.assertIn("Error", response.json())
        self.assertEqual(response.json()["Error"], "Usuario ingresado no existe")
    
    """
    ------------------------------------------------------------------------------------------------------
    PRUEBAS PARA POSTS
    ------------------------------------------------------------------------------------------------------
    """

    
    def test_get_user_posts(self):
        response = client.get(f"/{self.user_id}/posts")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Posts recientes", response.json())
    
    def test_get_post(self):
        response = client.get(f"/{self.user_id}/posts/{self.post_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Post", response.json())

    def test_update_post(self):
        updated_data = {
            "text": "Updated post content"
        }
        response = client.put(f"/{self.user_id}/posts/{self.post_id}/update", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Post actualizado", response.json())


    """
    ------------------------------------------------------------------------------------------------------
    PRUEBAS PARA COMENTARIOS DE POSTS
    ------------------------------------------------------------------------------------------------------
    """


    def test_get_comment(self):
        response = client.get(f"/{self.user_id}/posts/{self.post_id}/comment/{self.comment_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Comentario", response.json())

    def test_get_all_comments(self):
        response = client.get(f"/{self.user_id}/posts/{self.post_id}/comments/all")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Comentarios", response.json())

    def test_update_comment(self):
        updated_data = {
            "coment_text": "This is an updated test comment"
        }
        response = client.put(f"/{self.user_id}/posts/{self.post_id}/comment/{self.comment_id}/update", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Post actualizado", response.json())


    """
    ------------------------------------------------------------------------------------------------------
    PRUEBAS PARA REACCIONES DE POSTS
    ------------------------------------------------------------------------------------------------------
    """

    def test_get_reaction(self):
        response = client.get(f"/{self.user_id}/posts/{self.post_id}/reaction/{self.reaction_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Reaccion", response.json())

    def test_get_all_reactions(self):
        response = client.get(f"/{self.user_id}/posts/{self.post_id}/reactions/all")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Reacciones", response.json())

    def test_update_reaction(self):
        updated_data = {
            "reaccion": "love"
        }
        response = client.put(f"/{self.user_id}/posts/{self.post_id}/reaction/{self.reaction_id}/update", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Reaccion actualizada", response.json())


if __name__ == "__main__":
    unittest.main()


    """    
    @classmethod
    def setUpClass(cls):
        cls.user_token = None

    def test_01_register_nonexisting_user(self):
        response = client.post("/user", json=new_user)  # crear usuario exitoso
        self.assertEqual(response.status_code, 200, "Se esperaba éxito al registrar un nuevo usuario.")
    
    def test_02_register_existing_user(self):    
        response = client.post("/user", json=new_user)  # se registra de nuevo el user para generar un error
        self.assertEqual(response.status_code, 200, "El usuario ya existe, se esperaba un mensaje de error.")
    
    def test_03_register_user_field_required(self):    
        response = client.post("/user", json=incomplete_user)  # datos de usuario incompletos 
        self.assertEqual(response.status_code, 422, "Se esperaba un error de validación por campos incompletos.")
        error_response = response.json()
        self.assertIn("username", str(error_response), "Falta el campo 'username' en la respuesta de error.")
        self.assertIn("password", str(error_response), "Falta el campo 'password' en la respuesta de error.")
        self.assertIn("email", str(error_response), "Falta el campo 'email' en la respuesta de error.")

    
    def test_04_login_nonexisting_user(self): 
        response = client.post("/login", json=login_error)      # login con usuario no valido
        self.assertEqual(response.status_code, 200, "Se esperaba un error por usuario inexistente.")
    
    def test_05_login_field_required(self): 
        response = client.post("/login", json=incomplete_login)      # login con campos incompletos
        self.assertEqual(response.status_code, 422, "Se esperaba un error de validación por campos incompletos.")
        error_response = response.json()
        self.assertIn("username", str(error_response), "Falta el campo 'username' en la respuesta de error.")
        self.assertIn("password", str(error_response), "Falta el campo 'password' en la respuesta de error.")
    
    def test_06_login_existing_user(self):
        response = client.post("/login", json=login)
        self.assertEqual(response.status_code, 200, "Se esperaba un inicio de sesión exitoso.")
        
        response_data = response.json()
        self.assertIn("access_token", response_data, "Se esperaba recibir un 'access_token'.")
        # guardar el token para usarlo en otras pruebas
        TestAPI.user_token = response_data["access_token"]    
    
    
    def test_07_register_travel(self):                   
        response = client.post("/travels/travel", json=travel)
        self.assertEqual(response.status_code, 200, "Se esperaba un registro exitoso del viaje.")

    def test_08_get_travels(self):                   
        response = client.get("/travels")
        self.assertEqual(response.status_code, 200)
    
    
    def test_09_register_travel_error(self):
        response = client.post("/travels/travel", json=travel_error)  # Se intenta registrar un travel con un ID de usuario inválido
        self.assertEqual(response.status_code, 200, "Se esperaba un error por ID de usuario no existente.")  
    
    def test_10_register_destiny(self):
        response = client.post("/destinies/destiny", json=destiny)
        self.assertEqual(response.status_code, 200, "Se esperaba un registro exitoso del destino.")

    def test_11_get_destinies(self):                   
        response = client.get("/destinies")
        self.assertEqual(response.status_code, 200)
    
    
    def test_12_register_destiny_error(self):
        response = client.post("/destinies/destiny", json=destiny_error)  # Se intenta registrar un travel con un ID de usuario inválido
        self.assertEqual(response.status_code, 200, "Se esperaba un error por ID de usuario no existente.")  
    
    def test_13_register_wishlist(self):
        response = client.post("/wishlists/wishlist", json=wishlist)
        self.assertEqual(response.status_code, 200, "Se esperaba un registro exitoso del destino.")

    def test_14_get_wishlists(self):                   
        response = client.get("/wishlists")
        self.assertEqual(response.status_code, 200)
    
    
    def test_15_register_wishlist_error(self):
        response = client.post("/wishlists/wishlist", json=wishlist_error)  # Se intenta registrar un travel con un ID de usuario inválido
        self.assertEqual(response.status_code, 200, "Se esperaba un error por ID de usuario no existente.")  
    
    
    def test_16_logout(self):                   
        headers = {
            "Authorization": f"Bearer {TestAPI.user_token}"
        }

        response = client.post("/logout", json=travel, headers=headers)

        self.assertEqual(response.status_code, 200, "Se esperaba un logout exitoso.")
    """
