\c database;


-- FUNCIONES PARA USUARIO 


CREATE OR REPLACE FUNCTION public.register_user(IN _username VARCHAR, IN _password VARCHAR, IN _email VARCHAR)
RETURNS INTEGER
LANGUAGE 'plpgsql'
AS $$

DECLARE 
    username_exists BOOLEAN;
    email_exists BOOLEAN;
	result_id INTEGER;
BEGIN
	-- Verifica si el username existe
    SELECT EXISTS(SELECT 1 FROM users WHERE username = _username) INTO username_exists;

    -- Verifica si el email existe
    SELECT EXISTS(SELECT 1 FROM users WHERE email = _email) INTO email_exists;

    -- Solo registra si el username y email ingresados son unicos
    IF username_exists OR email_exists THEN
		RETURN -1; -- Username ya existe
	ELSE
    	INSERT INTO users (username, password, email)
    	VALUES (_username, _password, _email)
    	RETURNING id INTO result_id; -- Captura el id del usuario registrado
        RETURN result_id; -- Retorna el id del usuario registrado
	END IF;
END;
$$;


-- FUNCIONES PARA TRAVEL


CREATE OR REPLACE FUNCTION public.register_travel(
    IN _user_id INT,
    IN _title VARCHAR,
    IN _description TEXT,
    IN _ini_date DATE,
    IN _end_date DATE
)

RETURNS INTEGER
LANGUAGE 'plpgsql'
AS $$

DECLARE 
    user_exists BOOLEAN;
	result_id INTEGER;
BEGIN
	-- Verifica si el usuario existe
    SELECT EXISTS(SELECT 1 FROM users WHERE id = _user_id) INTO user_exists;

    -- Solo registra si el usuario existe
    IF user_exists THEN
		INSERT INTO travels (user_id, title, description, ini_date, end_date)
    	VALUES (_user_id, _title, _description, _ini_date, _end_date)
    	RETURNING id INTO result_id; -- Captura el id del travel registrado
        RETURN result_id; -- Retorna el id del travel registrado
	ELSE
        RETURN -1; -- Usuario asociado no existe
	END IF;
END;
$$;



-- FUNCIONES PARA Destinies


CREATE OR REPLACE FUNCTION public.register_destiny(
    IN _name VARCHAR,
    IN _description TEXT,
    IN _location VARCHAR,
    IN _url_image VARCHAR
)

RETURNS INTEGER
LANGUAGE 'plpgsql'
AS $$

DECLARE 
	result_id INTEGER;
BEGIN
    INSERT INTO destinies (name, description, location, url_image)
    VALUES (_name, _description, _location, _url_image)
    RETURNING id INTO result_id; -- Captura el id del travel registrado
    RETURN result_id; -- Retorna el id del travel registrado
END;
$$;



-- FUNCIONES PARA viajes destino


CREATE OR REPLACE FUNCTION public.register_destiny_travel(
    IN _travel_id INT,
    IN _destiny_id INT
)
RETURNS INTEGER  
LANGUAGE 'plpgsql'
AS $$
DECLARE 
    travel_exists BOOLEAN;
	destiny_exists BOOLEAN;
    result_id INTEGER;
BEGIN
    -- Verifica si el travel existe
    SELECT EXISTS(SELECT 1 FROM travels WHERE id = _travel_id) INTO travel_exists;

    -- Verifica si el destiny existe
    SELECT EXISTS(SELECT 1 FROM destinies WHERE id = _destiny_id) INTO destiny_exists;

    -- Solo registra si el usuario existe
    IF travel_exists AND destiny_exists THEN
        INSERT INTO destiny_travels (travel_id, destiny_id)
        VALUES (_travel_id, _destiny_id)
        RETURNING id INTO result_id; -- Captura el id del travel registrado
        RETURN result_id; -- Retorna el id del travel registrado
    ELSE
        RETURN -1;  
    END IF;
END;
$$;