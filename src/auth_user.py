import uuid
from fastapi import Depends, HTTPException
from src.db import get_session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.SessionModel import SessionUser
from src.models.UserModel import User



async def authChecker(key:uuid.UUID, session:AsyncSession=Depends(get_session)):
    ses = await session.scalar(select(SessionUser).where(SessionUser.key == key))
    if not ses:
        raise HTTPException(status_code=500, detail={"status_code":500, "details":"not correct key"})
    user = await session.scalar(select(User).where(User.id == ses.user_id))
    if not ses:
        raise HTTPException(status_code=500, detail={"status_code":500, "details":"such user does not exist"})
    return user