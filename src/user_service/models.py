from pydantic import BaseModel
from typing import Optional

class UserProfile(BaseModel):
    username: str
    role: str
    balance: float

class AdminUserView(BaseModel):
    username: str
    role: str
    balance: float
