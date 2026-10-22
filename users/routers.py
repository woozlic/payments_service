from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from users.schemas import UserRead, UserCreate
from users.service import create_user

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/register', response_model=UserRead, status_code=201)
async def register(data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await create_user(session, data)
    return user
