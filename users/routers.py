from fastapi import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from core.security import verify_password, create_access_token, get_current_user
from users.models import User
from users.schemas import UserRead, UserCreate
from users.service import create_user, get_user_by_email

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/register', response_model=UserRead, status_code=201)
async def register(data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await create_user(session, data)
    return user

@router.post('/login')
async def login(data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_email(session, data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token({'sub': str(user.id)})
    return {'access_token': token, "token_type": 'bearer'}

@router.get('/me', response_model=UserRead)
async def get_user_profile(user: User = Depends(get_current_user)):
    return user