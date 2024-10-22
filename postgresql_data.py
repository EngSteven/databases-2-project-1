import psycopg2
import os
from fastapi import *
from models.schemas import *


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            database=os.environ.get("DB_DB"),
        )

    def check_user_exists(self, user_id: int):
        try:
            cur = self.connection.cursor()

            cur.execute('SELECT EXISTS(SELECT 1 FROM users WHERE id = %s)', (user_id,))

            user_exists = cur.fetchone()[0]

            cur.close()

            if user_exists:
                return True
            else:
                return False

        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al verificar si el usuario existe: {e.pgerror}")
    
    
    def register_user(self, user: UserRegister):
        try:
            cur = self.connection.cursor()

            # Llamada al procedimiento almacenado para registrar al usuario
            cur.execute('SELECT register_user(%s,%s,%s)', (user.username, user.password, user.email))
            
            # Obtener el resultado
            user_id = cur.fetchone()[0]
                        
            self.connection.commit()
            cur.close()

            if user_id != -1:
                return {"id": user_id, "username": user.username, "password": user.password, "email": user.email}
            else:
                return "El nombre de usuario o email ingresado ya está asociado a otra cuenta"

        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al registrar el usuario: {e.pgerror}")
        

    def login(self, login: Login):
        try:
            cur = self.connection.cursor()

            cur.execute('SELECT login(%s,%s)', (login.username, login.password))
            
            status = cur.fetchone()[0]
                        
            self.connection.commit()
            cur.close()

            return status

        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error realizar el login: {e.pgerror}")


