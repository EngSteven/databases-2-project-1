\c database;


----------------------------------------- FUNCIONES PARA USUARIO -----------------------------------------


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


CREATE OR REPLACE FUNCTION public.get_user(IN _id INTEGER)
RETURNS TABLE(id INTEGER, username VARCHAR, email VARCHAR, is_active BOOLEAN)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    RETURN QUERY 
    SELECT users.id, users.username, users.email, users.is_active 
    FROM users 
    WHERE users.id = _id AND users.is_active = TRUE;
END;
$$;

CREATE OR REPLACE FUNCTION public.get_all_users()
RETURNS TABLE(id INTEGER, username VARCHAR, email VARCHAR, is_active BOOLEAN)
LANGUAGE 'plpgsql'
AS $$
BEGIN
    RETURN QUERY 
    SELECT users.id, users.username, users.email, users.is_active 
    FROM users 
    WHERE users.is_active = TRUE;
END;
$$;

CREATE OR REPLACE FUNCTION public.update_username(IN _id INTEGER, IN _username VARCHAR)
RETURNS BOOLEAN
LANGUAGE 'plpgsql'
AS $$
DECLARE
    username_exists BOOLEAN;
BEGIN
    -- Verifica si el nombre de usuario ya está tomado por otro usuario o si esta ingresando el mismo username
    SELECT EXISTS(SELECT 1 FROM users WHERE username = _username AND id != _id) INTO username_exists;

    IF username_exists THEN
        RETURN FALSE; -- Nombre de usuario ya existe para otro usuario
    ELSE
        UPDATE users
        SET username = _username
        WHERE id = _id AND is_active = TRUE;

        IF FOUND THEN
            RETURN TRUE; -- Actualización exitosa
        ELSE
            RETURN FALSE; -- Usuario no encontrado o desactivado
        END IF;
    END IF;
END;
$$;


CREATE OR REPLACE FUNCTION public.update_password(IN _id INTEGER, IN _password VARCHAR)
RETURNS BOOLEAN
LANGUAGE 'plpgsql'
AS $$
BEGIN
    UPDATE users
    SET password = _password
    WHERE id = _id AND is_active = TRUE;

    IF FOUND THEN
        RETURN TRUE; -- Contraseña actualizada exitosamente
    ELSE
        RETURN FALSE; -- Usuario no encontrado o desactivado
    END IF;
END;
$$;


CREATE OR REPLACE FUNCTION public.deactivate_user(IN _id INTEGER)
RETURNS BOOLEAN
LANGUAGE 'plpgsql'
AS $$
BEGIN
    UPDATE users
    SET is_active = FALSE
    WHERE id = _id AND is_active = TRUE;
    
    IF FOUND THEN
        RETURN TRUE; -- Usuario desactivado exitosamente
    ELSE
        RETURN FALSE; -- No se encontró el usuario o ya estaba desactivado
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION public.reactivate_user(IN _id INTEGER)
RETURNS BOOLEAN
LANGUAGE 'plpgsql'
AS $$
BEGIN
    UPDATE users
    SET is_active = TRUE
    WHERE id = _id AND is_active = FALSE;

    IF FOUND THEN
        RETURN TRUE; -- Usuario reactivado exitosamente
    ELSE
        RETURN FALSE; -- Usuario no encontrado o ya estaba activo
    END IF;
END;
$$;



CREATE OR REPLACE FUNCTION public.login(IN _username VARCHAR, IN _password VARCHAR)
RETURNS INTEGER
LANGUAGE 'plpgsql'
AS $$

DECLARE 
    user_exists BOOLEAN;
BEGIN

	-- Verifica si el usuario existe
	SELECT EXISTS (SELECT 1 FROM users WHERE username = _username AND password = _password) INTO user_exists;
	
    IF user_exists THEN
		RETURN 1; 		-- Los datos del usario son correctos
	ELSE
        RETURN 0; 		-- Los datos del usuario son incorrectos
	END IF;
END;
$$;
