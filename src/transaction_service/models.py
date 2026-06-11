from pydantic import BaseModel
from typing import Optional

class TransactionCreate(BaseModel):
    to_username: str
    amount: float
    description: Optional[str] = ""
