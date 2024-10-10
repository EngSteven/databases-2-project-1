import unittest
from fastapi.testclient import TestClient
from app import app 

# constantes 
ERROR_LESS_FIELDS = "error: no se han ingresado todos los campos requeridos"

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

print("\nPruebas\n")

class TestAPI(unittest.TestCase):   

    def test01_register_nonexisting_user(self):
        response = client.post("/user", json=new_user)
        self.assertEqual(response.status_code, 200)
    
    def test02_register_existing_user(self):    
        response = client.post("/user", json=new_user)  # se registra de nuevo el user para generar un error
        self.assertEqual(response.status_code, 200)

    def test03_register_user_field_required(self):    
        response = client.post("/user", json=incomplete_user)  # datos de usuario incompletos 
        
        self.assertEqual(response.status_code, 422)
        error_response = response.json()
        self.assertIn("password", str(error_response))
        self.assertIn("email", str(error_response))

    def test04_register_travel(self):                   
        response = client.post("/travel", json=travel)
        self.assertEqual(response.status_code, 200)

    def test05_register_travel_error(self):                   
        response = client.post("/travel", json=travel_error)    # se intenta registrar un travel a un user que no existe
        self.assertEqual(response.status_code, 200)

    def test06_register_destiny(self):
        response = client.post("/destiny", json=destiny)
        self.assertEqual(response.status_code, 200)

    def test07_register_destiny_travel(self):
        response = client.post("/destiny/travel", json=destiny_travel)
        self.assertEqual(response.status_code, 200)

    def test08_register_destiny_travel_error(self):
        response = client.post("/destiny/travel", json=destiny_travel_error)
        self.assertEqual(response.status_code, 200)
    

if __name__ == "__main__":
    unittest.main()