import bcrypt
import datetime

from binascii import Error
from fastapi import HTTPException

from src.config import config


# хэширование пароля
async def decode_password(password: str) -> bytes:
    new_password = bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())
    return new_password


# проверка пароля
async def check_password(password: str, old_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=old_password)
