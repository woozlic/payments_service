from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from users.models import User
from core.security import hash_password
from users.schemas import UserCreate


async def create_user(session: AsyncSession, data: UserCreate) -> User:
    existing = await get_user_by_email(session, data.email)
    if existing:
        raise HTTPException(status_code=409, detail='Email already registered')
    user = User(email=data.email, hashed_password=hash_password(data.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()
