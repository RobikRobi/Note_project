import bcrypt
from datetime import datetime, timezone

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import HTTPException, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.SessionModel import SessionUser
from src.models.UserModel import User
from src.db import get_session


bearer = HTTPBearer()

# хэширование пароля
async def hash_password(password: str) -> bytes:
    new_password = bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())
    return new_password


# проверка пароля
async def check_password(password: str, old_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=old_password)

# функция для проверки пользователя
async def authChecker(authorization: HTTPAuthorizationCredentials=Depends(bearer), session: AsyncSession=Depends(get_session)) -> User:
     # Проверяем наличие ключа
    if not authorization.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )

    # Ищем сессию по ключу
    stmt = select(SessionUser).where(SessionUser.key == authorization.credentials)
    session_user = await session.scalar(stmt)

    if not session_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session key"
        )

    # Проверяем срок действия сессии
    if session_user.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired"
        )

    # Получаем пользователя по user_id
    stmt_user = select(User).where(User.id == session_user.user_id)
    user = await session.scalar(stmt_user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user