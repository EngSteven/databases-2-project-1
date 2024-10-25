# Proyecto 1 de Base de datos 2 TEC (Red Social de Viajes)

## Autores: 
- Steven Sequeira 
- Brayton Solano
- Julian Madrigal

# Introducción

## Descripción

Este proyecto consiste en desarrollar el backend de una red social orientada a compartir experiencias de
viaje. El objetivo es que los usuarios puedan realizar publicaciones sobre sus viajes, agregar destinos a sus listas de objetivos de viaje y que otros usuarios interactúen con estas publicaciones mediante comentarios, likes y reacciones. Además, los usuarios podrán crear listas de destinos de viaje y asociar lugares a cada viaje. No se requiere frontend; el enfoque está en el backend, utilizando bases de datos Postgres, MongoDB y Redis, y desplegando todo el sistema mediante Docker y Docker Compose.

## Guía de instalación

-	Descargar el archivo .rar que contiene todos los archivos fuente del proyecto.
-	Abrir la localización en una terminal, se recomienda PowerShell o Bash.
-	Tener abierto y ejecutando el Docker Desktop.
-	En la terminal, insertar el comando docker-compose up –-build
NOTA: Todas las librerías y servicios necesarios se encuentran en el docker-compose.

## Funcionalidades principales 

- 

## Herramientas principales usadas
- 

## Enlace a la documentación de la API 


# Comandos 

## Construye y ejecuta el contenedor de docker
``` bash
docker-compose up --build
```

## Ejecutar el módulo de pruebas unitarias
### Primero corra el contenedor en segundo plano
``` bash
docker-compose up -d --build
```

### Ejecutar las pruebas unitarias
``` bash
docker compose exec webapp poetry run coverage run -m unittest test-api -v
```

### Visualizar el reporte de la covertura de las pruebas unitarias
``` bash
docker compose exec webapp poetry run coverage report
```

# Endpoints usando Postman

## Registrar usuario
Se selecciona un método POST y se ingresa en un body de tipo raw el nombre de usuario, la contraseña, y el email.
### Ruta
``` bash
localhost:8000/user
```
### Body de ejemplo
``` bash
{
    "username": "sebas2043",
    "password": "12345",
    "email": "sebassequeira12@gmail.com"
}
```

## Inicio de sesión
Se selecciona un método POST y se ingresa en un body de tipo raw el nombre de usuario y la contraseña
### Ruta
``` bash
localhost:8000/login
```
### Body de ejemplo
``` bash
{
    "username": "sebas2043",
    "password": "12345"
}
```

Si todo sale bien verá un token de autenticación como retorno. Guardelo para poder usarlo en las demás pruebas.

## Registrar un viaje
Método: POST
### Ruta 
``` bash
localhost:8000/travels/travel
``` 
### Body de ejemplo
``` bash
{
    "user_id": 1,
    "trip_name": "Vacaciones en la playa",
    "description": "Un viaje a la playa con amigos.",
    "places_visited": ["object_id_1", "object_id_2"]
}
```

## Listar los viajes
Método: GET
### Ruta 
``` bash
localhost:8000/travels
``` 

## Registrar un destino
Método: POST
### Ruta 
``` bash
localhost:8000/destinies/destiny
``` 
### Body de ejemplo
``` bash
{
    "user_id": 1,
    "destiny_name": "Coliseo Romano",
    "description": "",
    "country": "Italia",
    "city": "Roma",
    "images": ["https://example.com/coliseo-romano.jpg"]
}
```

## Listar los destinos
Método: GET
### Ruta 
``` bash
localhost:8000/destinies
```

## Registrar una lista de deseos 
Método: POST
### Ruta 
``` bash
localhost:8000/wishlists/wishlist
``` 
### Body de ejemplo
``` bash
{
    "user_id": 1,
    "list_name": "Lista 1",
    "destinies": ["6716ad37f153e408a145d417", "6716ad44f153e408a145d418"]
}
```

## Listar todas las listas de deseos
Método: GET
### Ruta 
``` bash
localhost:8000/wishlists
```

## Realizar un follow a una lista de deseo 
Método: POST
### Ruta 
``` bash
localhost:8000/wishlists/follow
``` 
### Body de ejemplo
``` bash
{
    "user_id": 1,
    "wishlist_id": "67170c9441c861f1f4124730"
}
```

## Quitar un follow a una lista de deseo 
Método: DELETE
### Ruta 
``` bash
localhost:8000/wishlists/follow
``` 
### Body de ejemplo
``` bash
{
    "user_id": 1,
    "wishlist_id": "67170c9441c861f1f4124730"
}
```

## Agregar un destino a una lista de deseos
Método: POST
### Ruta 
``` bash
localhost:8000/wishlists/destiny
``` 
### Body de ejemplo
``` bash
{
    "user_id": 1,
    "wishlist_id": "67170c9441c861f1f4124730",
    "destiny_id": "67170c9441c861f1f412472f"
}
```


## Quitar un destino a una lista de deseos
Método: DELETE
### Ruta 
``` bash
localhost:8000/wishlists/destiny
``` 
### Body de ejemplo
``` bash
{
    "user_id": 1,
    "wishlist_id": "67170c9441c861f1f4124730",
    "destiny_id": "67170c9441c861f1f412472f"
}
```


