import redis
import jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

# Clave secreta y algoritmo de JWT
SECRET_KEY = "tu_clave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Expiración del token en minutos


# Configurar Redis
redis_client = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

# Esquema OAuth2 para extraer el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para verificar el token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")
        
        # Verificar si el token está en Redis
        redis_token = redis_client.get(username)
        if redis_token is None or redis_token != token:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
   
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
