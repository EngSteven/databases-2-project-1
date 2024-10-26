CREATE DATABASE database;

\c database

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

INSERT INTO users (username, password, email, is_active)
VALUES ('nombre_usuario', 'contraseña_segura', 'correo@example.com', TRUE);
