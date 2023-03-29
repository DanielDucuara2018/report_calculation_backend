from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CurrencyPairRequest(BaseModel):

    symbol: Optional[str] = None
    user_id: Optional[str] = None
    quantity: Optional[float] = None


@dataclass
class CurrencyPairResponse:  # TODO check if it can use BaseModel

    symbol: Optional[str] = None
    user_id: Optional[str] = None
    price: Optional[str] = None
    purchases: Optional[list] = None
    quantity: Optional[float] = None
    creation_date: Optional[datetime] = None
    update_date: Optional[datetime] = None
