from typing import Optional

from pydantic import BaseModel


class User(BaseModel):

    telegram_id: Optional[str] = None
    investment_euros: Optional[float] = None
    invesment_usd: Optional[float] = None
    savings_euros: Optional[float] = None
    savings_usd: Optional[float] = None
