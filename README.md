# TC01 DockerRestAPI

# Gestor de Tareas con Flask y PostgreSQL

Este proyecto es una sistema rest-api para la gestión y autenticación de usuarios, así como para la publicación de diferentes tipos de posts.

## Funcionalidades principales 

- Autenticación de usuarios mediante JWT.
- Creación, actualización, lectura y eliminación de usuarios.
- Escritura de posts, tales como imágenes, textos y videos.
- Visualización de tareas por usuario y por ID de tarea.

## Herramientas principales usadas
- Python como lenguaje principal para el backend.
- Fastapi como framework para la gestión del sistema.
- JWT para autenticación.
- Postman para la documentación de los endpoints.
- Doker y Dockercompose.
- Postgresql para la base de datos.

## Enlace a la documentación de la API 
[Click here](https://documenter.getpostman.com/view/37666062/2sAXjDdudZ)

# Commandos 

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

## Inicio de sesión
Se selecciona un método POST y se ingresa en un body de tipo x-www-form-urlencoded, con una key username y otra key password
### Request
``` bash
localhost:8000/login
```
### Ejemplo
<img src="login-example.png"/>

## Registrar usuario
Se selecciona un método POST y se ingresa en un body de tipo raw el nombre de usuario, la contraseña, y el rol.
### Request
``` bash
localhost:8000/register
```
### Body de ejemplo
``` bash
{
    "username": "alex27",
    "password": "holamundo",
    "role": "editor"
}
```

## Obtener usuarios
Se selecciona un método GET.
### Request
``` bash
localhost:8000/read
```

## Eliminar un usuario mediante el nombre de usuario
Se selecciona un método DELETE y se ingresa en un body de tipo raw el nombre de usuario.
### Request
``` bash
localhost:8000/delete
```
### Body de ejemplo
``` bash
{
    "username": "steven"
}
```

## Eliminar un usuario mediante el id del usuario
Se selecciona un método DELETE y se ingresa en un body de tipo raw el id.
### Request
``` bash
localhost:8000/id/delete
```
### Body de ejemplo
``` bash
{
    "id": 10
}
```

## Actualizar usuario mediante id
Se selecciona un método PUT y se ingresa en un body de tipo raw el id de usuario, el nombre de usuario, la contraseña y el role.
### Request
``` bash
localhost:8000/id/update
```
### Body de ejemplo
``` bash
{
    "id" : 10,
    "username": "alex27",
    "password": "holamundo",
    "role": "editor"
}
```

## Actualizar usuario mediante username
Se selecciona un método PUT y se ingresa en un body de tipo raw el nombre de usuario, la contraseña y el role.
### Request
``` bash
localhost:8000/update
```
### Body de ejemplo
``` bash
{
    "username": "alex27",
    "password": "holamundo",
    "role": "editor"
}
```

## Escritura de posts
Se selecciona un método POST y se ingresa en un body de tipo form-data, con una key file, de tipo File y se carga en el Value el archivo (texto, imágen o video) requerido desde su máquina. 

Ese archivo debe estar en su Postman/files, normalmente ubicado en: C:\Users\username\Postman\files

### Request
``` bash
localhost:8000/posts
```
### Ejemplo
<img src="posts-example.png"/>
