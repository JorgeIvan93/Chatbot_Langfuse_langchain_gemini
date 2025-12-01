from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    """
    if len(plain_password) > 72:
        # bcrypt_only supports up to 72 bytes - enforce limit for safety
        raise ValueError("Password too long (max 72 characters)")
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a bcrypt hash.
    """
    return pwd_context.verify(plain_password, hashed_password)
