from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = "sua-chave-secreta"  # mova para .env
ALGORITHM  = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"])

def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

def verificar_senha(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def criar_token(data: dict, expires_minutes: int = 60) -> str:
    payload = data | {"exp": datetime.utcnow() + timedelta(minutes=expires_minutes)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
