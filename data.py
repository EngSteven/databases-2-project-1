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
    
    """
    def login(self, login: Login):
        try:
            cur = self.connection.cursor()

            # Llamada al procedimiento almacenado para registrar al usuario
            cur.execute('SELECT login(%s,%s)', (login.username, login.password))
            
            # Obtener el resultado, por ejemplo, el ID del usuario registrado
            status = cur.fetchone()[0]
                        
            self.connection.commit()
            cur.close()

            if status == 1:
                return "Login exitoso"
            else:
                return "Login fallido"

        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error realizar el login: {e.pgerror}")

    """


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

    """
    def obtener_usuarios(self):
        try:
            cur = self.connection.cursor()

            # Llamada al procedimiento almacenado para registrar al usuario
            cur.execute('SELECT obtener_usuarios()')
            
            # Obtener el resultado, por ejemplo, el ID del usuario registrado
            data = cur.fetchall()
                        
            self.connection.commit()
            cur.close()

            if data != None:
                return data
            else:
                return "No se ha podido obtener los datos"

        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al registrar obtener los usuarios: {e.pgerror}")
    
    def obtener_usuario(self, username: str):
        cur = self.connection.cursor()
        # Supongamos que tienes una tabla llamada 'usuarios'
        cur.execute("SELECT username, password, role FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user:
            return {
                "username": user[0],
                "password": user[1],  # La contraseña hasheada
                "role": user[2]
            }
        return None

    def eliminar_usuario_por_id(self, user_id: UserId):
        try:
            status = 0
            cur = self.connection.cursor()

            # Llamada a la funcion de la base de datos para eliminar al usuario
            cur.execute("SELECT eliminar_usuario_por_id(%s);", (user_id.id,))
            status = cur.fetchone()[0]
            self.connection.commit()
            cur.close()
            
            if status == 1:
                return "Usuario eliminado correctamente"
            else: 
                return "El id del usuario ingresado no existe"
                
        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar el usuario: {e.pgerror}")
        
    def actualizar_usuario_por_id(self, user: User):
        try:
            status = 0
            cur = self.connection.cursor()

            # Llamada a la funcion de la base de datos para actualizar al usuario
            cur.execute("SELECT actualizar_usuario_por_id(%s, %s, %s, %s);", (user.id, user.username, user.password, user.role.value))
            status = cur.fetchone()[0]
            self.connection.commit()
            cur.close()
            
            if status == 1:
                return "Usuario actualizado correctamente"
            else: 
                return "El id del usuario ingresado no existe"
                
        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar el usuario: {e.pgerror}")
    """

    def register_travel(self, travel: TravelRegister):
        try:
            cur = self.connection.cursor()

            # Llamada al procedimiento almacenado para registrar al usuario
            cur.execute('SELECT register_travel(%s,%s,%s,%s,%s)', (travel.user_id, travel.title, travel.description, travel.ini_date, travel.end_date))
            
            # Obtener el resultado
            travel_id = cur.fetchone()[0]
                        
            self.connection.commit()
            cur.close()

            if travel_id != -1:
                return {"id": travel_id, "user_id": travel.user_id, "title": travel.title, "description": travel.description, "ini_date": travel.ini_date, "end_date": travel.end_date}
            else:
                return "Usuario asociado no existe"

        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al registrar viaje: {e.pgerror}")



    def register_destiny(self, destiny: DestinyRegister):
        try:
            cur = self.connection.cursor()

            # Llamada al procedimiento almacenado para registrar al usuario
            cur.execute('SELECT register_destiny(%s,%s,%s,%s)', (destiny.name, destiny.description, destiny.location, destiny.url_image))
            
            # Obtener el resultado
            destiny_id = cur.fetchone()[0]
                        
            self.connection.commit()
            cur.close()

            return {"id": destiny_id, "name": destiny.name, "description": destiny.description, "location": destiny.location, "url_image": destiny.url_image}

        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al registrar un destino: {e.pgerror}")
    
    
    def register_destiny_travel(self, destiny_travel: DestinyTravelRegister):
        try:
            cur = self.connection.cursor()

            # Llamada al procedimiento almacenado para registrar al usuario
            cur.execute('SELECT register_destiny_travel(%s,%s)', (destiny_travel.travel_id, destiny_travel.destiny_id))
            
            # Obtener el resultado
            destiny_travel_id = cur.fetchone()[0]
                        
            self.connection.commit()
            cur.close()

            if destiny_travel_id != -1: 
                return {"id": destiny_travel_id, "travel_id": destiny_travel.travel_id, "destiny_id": destiny_travel.destiny_id}
            else:
                return "El viaje o destino no existen"
        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al registrar un destino a un viaje: {e.pgerror}")
    
        
        
    