from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from core.db import get_session
from users.routers import router

app = FastAPI()
app.include_router(router)


@router.get('/me')
async def me(session: AsyncSession = Depends(get_session)):
    return {'hello': 'world'}
