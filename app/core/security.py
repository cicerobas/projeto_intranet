from datetime import datetime, timedelta, timezone

from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status
from app.core.settings import get_settings

ALGORITHM = "HS256"
TOKEN_EXPIRES = 60

settings = get_settings()
password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=TOKEN_EXPIRES)
    to_encode.update({"exp": expire, "nbf": now})
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)


def decode_access_token(access_token: str) -> dict | None:
    try:
        payload = jwt.decode(access_token, settings.secret_key, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        return None
