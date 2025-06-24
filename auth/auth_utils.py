from passlib.context import CryptContext
from uuid import uuid4
from datetime import datetime, timedelta
from db.models import SessionToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_session_token(user_email: str, db):
    token = str(uuid4())
    expires_at = datetime.utcnow() + timedelta(days=1)
    session = SessionToken(
        token=token,
        user_email=user_email,
        expires_at=expires_at
    )
    db.add(session)
    db.commit()
    return token

def verify_session_token(token: str, db):
    session = db.query(SessionToken).filter(SessionToken.token == token).first()
    if not session or session.expires_at < datetime.utcnow():
        return None
    return session.user
