from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CurrencyPairRequest(BaseModel):

    quantity: Optional[float] = None
    description: Optional[str] = None


class CurrencyPairResponse(CurrencyPairRequest):

    symbol: Optional[str] = None
    price: Optional[float] = None
    creation_date: Optional[datetime] = None
    update_date: Optional[datetime] = None


@dataclass
class CurrencyPairBinanceResponse:

    symbol: Optional[str] = None
    price: Optional[str] = None
