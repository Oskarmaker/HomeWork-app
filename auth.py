from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext


SECRET_KEY = "iamlordofnowhere"  # Секретный ключ для подписи токена
ALGORITHM = "HS256" # Алгоритм шифрования
EXPIRE_MINUTES = 60 # Срок жизни токена в минутах

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Объект для хэширования паролей

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data):
    payload = data.copy()
    payload['exp'] = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
