from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Session
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    hashed_password = Column(String, nullable=False)
    name = Column(String, default="")
    avatar = Column(String, default="")
    is_verified = Column(Boolean, default=False)

    @classmethod
    def get_by_email(cls, db: Session, email: str):
        return db.query(cls).filter(cls.email == email).first()

    @classmethod
    def create(cls, db: Session, email: str, hashed_password: str):
        user = cls(email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update_profile(self, db: Session, name: str, avatar: str):
        self.name = name
        self.avatar = avatar
        db.commit()
        return self

    def change_password(self, db: Session, new_hashed_password: str):
        self.hashed_password = new_hashed_password
        db.commit()


class SessionToken(Base):
    __tablename__ = "session_tokens"

    token = Column(String, primary_key=True, index=True)
    user_email = Column(String, ForeignKey("users.email"))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

    user = relationship("User")

    @classmethod
    def get_valid_token(cls, db: Session, token: str):
        session = db.query(cls).filter(cls.token == token).first()
        if session and session.expires_at > datetime.utcnow():
            return session
        return None

    @classmethod
    def create_token(cls, db: Session, token: str, user_email: str, expires_at: datetime):
        session = cls(token=token, user_email=user_email, expires_at=expires_at)
        db.add(session)
        db.commit()
        return session

class MagicLinkToken(Base):
    __tablename__ = "magic_link_tokens"

    token = Column(String, primary_key=True, index=True)
    email = Column(String, ForeignKey("users.email"), nullable=False)
    expires_at = Column(DateTime, nullable=False)

    @classmethod
    def create(cls, db, email: str, token: str, expires_at: datetime):
        link = cls(token=token, email=email, expires_at=expires_at)
        db.add(link)
        db.commit()
        return link

    @classmethod
    def get_valid_token(cls, db, token: str):
        link = db.query(cls).filter(cls.token == token).first()
        if link and link.expires_at > datetime.utcnow():
            return link
        return None