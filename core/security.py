import hashlib
import base64
import bcrypt


def hash_password(password: str) -> str:
    sha256 = hashlib.sha256(password.encode()).digest()
    b64 = base64.b64encode(sha256)
    return bcrypt.hashpw(b64, bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    sha256 = hashlib.sha256(plain.encode()).digest()
    b64 = base64.b64encode(sha256)
    return bcrypt.checkpw(b64, hashed.encode())