from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserRequest(BaseModel):

    telegram_id: Optional[str] = None
    investment_euros: Optional[float] = None
    savings_euros: Optional[float] = None
    description: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None


class UserResponse(UserRequest):

    user_id: Optional[str] = None
    update_date: Optional[datetime] = None
    creation_date: Optional[datetime] = None


class Token(BaseModel):
    access_token: str
    token_type: str
