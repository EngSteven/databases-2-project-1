import unittest
from fastapi.testclient import TestClient
from app import app 

client = TestClient(app)

new_user = {
    "username": "steven1234",
    "password": "1234",
    "email": "steven1234@gmail.com"
}

nonexisting_user = {
    "username": "sofia506",
    "password": "1324",
    "email": "sofia@gmail.com"
}

incomplete_user = {
    "username": "steven12345",
    "password": "1234"
}

login = {
    "username": "steven1234",
    "password": "1234"
}

login_error = {
    "username": "steven12345",
    "password": "1234"
}

incomplete_login = {
    "username": "steven12345"
}

travel = {
    "user_id": 1,
    "trip_name": "Vacaciones en la playa",
    "description": "Un viaje a la playa con amigos.",
    "places_visited": ["object_id_1", "object_id_2"]
}

travel_error = {
    "user_id": -1,
    "trip_name": "Vacaciones en la playa",
    "description": "Un viaje a la playa con amigos.",
    "places_visited": ["object_id_1", "object_id_2"]
}

destiny = {
    "user_id": 1,
    "destiny_name": "Coliseo Romano",
    "description": "",
    "country": "Italia",
    "city": "Roma",
    "images": ["https://example.com/coliseo-romano.jpg"]
}

destiny_error = {
    "user_id": -1,
    "destiny_name": "Coliseo Romano",
    "description": "",
    "country": "Italia",
    "city": "Roma",
    "images": ["https://example.com/coliseo-romano.jpg"]
}

wishlist = {
    "user_id": 1,
    "list_name": "Lista 1",
    "destinies": ["6716ad37f153e408a145d417", "6716ad44f153e408a145d418"]
}

wishlist_error = {
    "user_id": -1,
    "list_name": "Lista 1",
    "destinies": ["6716ad37f153e408a145d417", "6716ad44f153e408a145d418"]
}

print("\n Ejecutando pruebas unitarias \n")

class TestAPI(unittest.TestCase):   
    
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

    """
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
    """
    
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
    
    """
    def test_16_logout(self):                   
        headers = {
            "Authorization": f"Bearer {TestAPI.user_token}"
        }

        response = client.post("/logout", json=travel, headers=headers)

        self.assertEqual(response.status_code, 200, "Se esperaba un logout exitoso.")
    """
    
if __name__ == "__main__":
    unittest.main()
