# Proyecto 1 de Base de datos 2 TEC (Red Social de Viajes)

## Autores: 
- Steven Sequeira 
- Brayton Solano
- Julian Madrigal

# Introducción

## Descripción

Este proyecto consiste en desarrollar el backend de una red social orientada a compartir experiencias de
viaje. El objetivo es que los usuarios puedan realizar publicaciones sobre sus viajes, agregar destinos a sus listas de objetivos de viaje y que otros usuarios interactúen con estas publicaciones mediante comentarios, likes y reacciones. Además, los usuarios podrán crear listas de destinos de viaje y asociar lugares a cada viaje. No se requiere frontend; el enfoque está en el backend, utilizando bases de datos Postgres, MongoDB y Redis, y desplegando todo el sistema mediante Docker y Docker Compose.


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

## 1. Registrar usuario
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

## 2. Inicio de sesión
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

## 3. Travel
Se selecciona un método POST y se ingresa en un body de tipo raw los datos como el siguiente ejemplo
### Body de ejemplo
``` bash
{
    "user_id": 2,
    "title": "Vacaciones en la playa",
    "description": "Un viaje a la playa con amigos.",
    "ini_date": "2024-10-01",
    "end_date": "2024-10-10"
}
```

### Ruta 
``` bash
localhost:8000/travel
```


