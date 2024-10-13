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
    "title": "Vacaciones en la playa 2",
    "description": "Un viaje a la playa con amigos.",
    "ini_date": "2024-10-01",
    "end_date": "2024-10-10"
}

travel_error = {
    "user_id": -1,
    "title": "Vacaciones en la playa 2",
    "description": "Un viaje a la playa con amigos.",
    "ini_date": "2024-10-01",
    "end_date": "2024-10-10"
}

destiny = {
    "name": "Playa de Copacabana 2",
    "description": "Una de las playas más famosas de Brasil, conocida por su arena blanca y vibrante vida nocturna.",
    "location": "Río de Janeiro, Brasil",
    "url_image": "https://example.com/images/copacabana.jpg"
}

destiny_travel = {
    "travel_id": 1,
    "destiny_id": 1
}

destiny_travel_error = {
    "travel_id": -1,
    "destiny_id": 1
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
        headers = {
            "Authorization": f"Bearer {TestAPI.user_token}"
        }

        response = client.post("/travel", json=travel, headers=headers)

        self.assertEqual(response.status_code, 200, "Se esperaba un registro exitoso del viaje.")

    def test_08_register_travel_bad_token(self):                   

        headers = {
            "Authorization": "Bearer invalid_token_xd"
        }

        response = client.post("/travel", json=travel, headers=headers)

        self.assertEqual(response.status_code, 401, "Se esperaba un error por token inválido.")
    
    
    def test_09_register_travel_error(self):
        headers = {
            "Authorization": f"Bearer {TestAPI.user_token}"  # Envía el token de autenticación
        }
        
        response = client.post("/travel", json=travel_error, headers=headers)  # Se intenta registrar un travel con un ID de usuario inválido
        self.assertEqual(response.status_code, 200, "Se esperaba un error por ID de usuario no existente.")  
    
    def test_10_register_destiny(self):
        response = client.post("/destiny", json=destiny)
        self.assertEqual(response.status_code, 200, "Se esperaba un registro exitoso del destino.")

    def test_11_register_destiny_travel(self):
        response = client.post("/destiny/travel", json=destiny_travel)
        self.assertEqual(response.status_code, 200, "Se esperaba un registro exitoso de la relación entre destino y viaje.")

    def test_12_register_destiny_travel_error(self):
        response = client.post("/destiny/travel", json=destiny_travel_error)
        self.assertEqual(response.status_code, 200, "Se esperaba un error por ID de viaje inválido.")
    

if __name__ == "__main__":
    unittest.main()
