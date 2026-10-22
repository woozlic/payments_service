import hashlib
import base64

import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import get_session
from users.models import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        session: AsyncSession = Depends(get_session),
) -> User:
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=["HS256"])
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def hash_password(password: str) -> str:
    sha256 = hashlib.sha256(password.encode()).digest()
    b64 = base64.b64encode(sha256)
    return bcrypt.hashpw(b64, bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    sha256 = hashlib.sha256(plain.encode()).digest()
    b64 = base64.b64encode(sha256)
    return bcrypt.checkpw(b64, hashed.encode())


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm='HS256')
