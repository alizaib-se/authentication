from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    name: str
    avatar: str
    is_verified: bool

    class Config:
        orm_mode = True

class UpdateProfile(BaseModel):
    name: str
    avatar: str

class ChangePassword(BaseModel):
    current_password: str
    new_password: str
