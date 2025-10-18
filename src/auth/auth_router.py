from fastapi import APIRouter, Depends, HTTPException, Path, status
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
import uuid

from src.models.UserModel import User
from src.models.SessionModel import SessionUser
from src.auth.auth_shema import RegisterUser, LoginUser, UpdateUser, UserShema
from src.auth.auth_utilits import hash_password, check_password
from src.db import get_session
from src.auth.auth_utilits import authChecker


app = APIRouter(prefix="/users", tags=["Users"])



# регистрацияe
@app.post("/reg", status_code=201)
async def register_user(data:RegisterUser, session:AsyncSession = Depends(get_session)):
    
   # Проверяем, существует ли пользователь
    existing_user = await session.scalar(select(User).where(User.login == data.login))
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"status": 409, "message": "User already exists"}
        )
    
    # Хэшируем пароль
    hashed_password = await hash_password(data.password)

    # Создаём пользователя
    user = User(login=data.login, password=hashed_password, name=data.name)
    session.add(user)
    await session.flush()
    await session.refresh(user)

    # Создаём сессию для пользователя
    session_key = uuid.uuid4()
    session_user = SessionUser(user_id=user.id, key=session_key, expires_at=datetime.now(timezone.utc) + timedelta(hours=24))
    session.add(session_user)
    
    await session.commit()

    # Возвращаем ключ авторизации
    return {
        "message": "Registration successful",
        "user": {"id": user.id, "login": user.login, "name": user.name},
        "session_key": str(session_key)
    }

# авторизация
@app.post("/auth")
async def auth_user(data: LoginUser, session: AsyncSession = Depends(get_session)):
    user = await session.scalar(select(User).where(User.login == data.login))

    # если пользователь не найден или пароль неверный
    if not user or not await check_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": 401, "details": "Invalid login or password"}
        )

    # удаляем старые сессии пользователя
    await session.execute(delete(SessionUser).where(SessionUser.user_id == user.id))

    # создаём новую сессию
    session_key = uuid.uuid4()
    new_session = SessionUser(user_id=user.id, key=session_key, expires_at=datetime.now(timezone.utc) + timedelta(hours=24))
    session.add(new_session)

    # сохраняем изменения
    await session.commit()

    return {"key": str(session_key)}


# получение авторизованного пользователя
@app.get("/me")
async def me(current_user: User = Depends(authChecker)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "login": current_user.login
    }

# изменение данных пользователя
@app.put("/update", response_model=UserShema)
async def user_update(data: UpdateUser, me: User = Depends(authChecker), session: AsyncSession=Depends(get_session)):
    await session.refresh(me)
    if data.login:
        me.login = data.login
    if data.name:
        me.name = data.name
    await session.commit()
    await session.refresh(me)

    return me

@app.delete("/delete/{user_id}")
async def user_delete(user_id: int = Path(..., gt=0), 
                      current_user: User = Depends(authChecker), 
                      session: AsyncSession = Depends(get_session)):
# Проверяем, существует ли пользователь
    user = await session.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Удаляем все сессии пользователя
    await session.execute(delete(SessionUser).where(SessionUser.user_id == user_id))

    # Удаляем пользователя
    await session.delete(user)
    await session.commit()

    return {"message": f"User with ID {user_id} and all related sessions have been deleted"}