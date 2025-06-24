from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import User, SessionToken
from routes import api_requests as schema
from auth import auth_utils
from common.logger import setup_logger
from datetime import datetime, timedelta
from uuid import uuid4
from random import randint
from db.models import MagicCodeToken


router = APIRouter()
log = setup_logger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    session = SessionToken.get_valid_token(db, token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    return session.user

@router.post("/signup", response_model=schema.UserOut)
def signup(data: schema.UserCreate, db: Session = Depends(get_db)):
    if User.get_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email exists")
    user = User.create(db, data.email, auth_utils.hash_password(data.password))
    log.info(f"User signed up: {user.email}")
    return user

@router.post("/login")
def login(data: schema.UserLogin, db: Session = Depends(get_db)):
    user = User.get_by_email(db, data.email)
    if not user or not auth_utils.verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = str(uuid4())
    expires = datetime.utcnow() + timedelta(days=1)
    SessionToken.create_token(db, token, user.email, expires)
    log.info(f"User logged in: {user.email}")
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schema.UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/update-profile")
def update_profile(data: schema.UpdateProfile, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.update_profile(db, data.name, data.avatar)
    log.info(f"Profile updated for user: {current_user.email}")
    return {"message": "Profile updated"}

@router.post("/change-password")
def change_password(data: schema.ChangePassword, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not auth_utils.verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=403, detail="Wrong password")
    current_user.change_password(db, auth_utils.hash_password(data.new_password))
    log.info(f"Password changed for user: {current_user.email}")
    return {"message": "Password changed"}

@router.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Service is healthy"}


@router.post("/request-magic-code")
def request_magic_code(data: schema.RequestMagicCode, db: Session = Depends(get_db)):
    user = User.get_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    code = f"{randint(100000, 999999)}"
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    MagicCodeToken.create(db, user.id, code, expires_at)

    subject = "Your Login Code"
    from email_utils.template_registry import get_email_body
    from email_utils.sender_factory import get_email_sender
    body = get_email_body("magic_code", code=code)
    get_email_sender().send_email(user.email, subject, body)

    return {"message": "Magic code sent"}


@router.post("/verify-magic-code")
def verify_magic_code(data: schema.VerifyMagicCode, db: Session = Depends(get_db)):
    user = MagicCodeToken.verify(db, data.code)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired code")

    token = str(uuid4())
    expires = datetime.utcnow() + timedelta(days=1)
    SessionToken.create_token(db, token, user.email, expires)
    return {"access_token": token, "token_type": "bearer"}
