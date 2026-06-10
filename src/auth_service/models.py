from pydantic import BaseModel, validator
from typing import Optional

class UserRegister(BaseModel):
    username: str
    password: str
    role: Optional[str] = "customer"

    @validator('username')
    def username_valid(cls, v):
        if len(v) < 3 or len(v) > 50:
            raise ValueError('Username must be between 3 and 50 characters')
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric only')
        return v

    @validator('password')
    def password_valid(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

    @validator('role')
    def role_valid(cls, v):
        if v not in ['customer', 'admin']:
            raise ValueError('Role must be customer or admin')
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    role: str
    balance: float = 1000.0
