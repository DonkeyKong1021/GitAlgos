from datetime import datetime, timedelta
from typing import Any, Dict

from cryptography.fernet import Fernet
from passlib.context import CryptContext

from app.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fernet = Fernet(settings.fernet_secret.encode())


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def encrypt_secret(secret: str) -> bytes:
    return fernet.encrypt(secret.encode())


def decrypt_secret(secret_encrypted: bytes) -> str:
    return fernet.decrypt(secret_encrypted).decode()
