from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserRequest(BaseModel):

    telegram_id: Optional[str] = None
    investment_euros: Optional[float] = None
    savings_euros: Optional[float] = None


class UserResponse(UserRequest):

    user_id: Optional[str] = None
    currency_pairs: Optional[list] = None
    purchases: Optional[list] = None
    update_date: Optional[datetime] = None
    creation_date: Optional[datetime] = None
