from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import uuid

from src.models.UserModel import User
from src.models.SessionModel import SessionUser
from src.auth.auth_shema import RegisterUser
from src.auth.auth_utilits import decode_password, check_password
from src.db import get_session
from src.auth_user import authChecker


app = APIRouter(prefix="/users", tags=["Users"])



# регистрация
@app.post("/reg")
async def register_user(data:RegisterUser, session:AsyncSession = Depends(get_session)):
    
    isUserEx = await session.scalar(select(User).where(User.login == data.login))
    
    if isUserEx:
        raise HTTPException(status_code=411, detail={
        "status":411,
        "data":"user is exists"
        })
        
    data_dict = data.model_dump()
        
    data_dict["password"] = await decode_password(password=data.password)
    
    user = User(**data_dict)
    session.add(user) 
    await session.flush()

    session_key = uuid.uuid4()
    user_id = user.id
    session_user = SessionUser(user_id = user.id, key = session_key)
    session.add(session_user)
    session.commit()
    return {"key":session_key}

# получение авторизованного пользователя
@app.get("/me")
async def me(me: User = Depends(authChecker)):
     return me.name

# авторизация
# @app.post("/login")
# async def login_user(data:LoginUser, session:AsyncSession = Depends(get_session)):
#     user = await session.scalar(select(User).where(User.email == data.email))

#     if user:
#         if await check_password(password=data.password, old_password=user.password):
#             user_token = await create_access_token(user_id=user.id)
#             return {"token":user_token}

#     raise HTTPException(status_code=401, detail={
#                 "details":"user is not exists",
#                 "status":401
#         })


