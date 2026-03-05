from datetime import datetime, timedelta
from jose import jwt
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-insecure-secret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

_expire_minutes_raw = os.getenv("JWT_EXPIRE_MINUTES", "60")
try:
    EXPIRE_MINUTES = int(_expire_minutes_raw)
except (TypeError, ValueError):
    EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
