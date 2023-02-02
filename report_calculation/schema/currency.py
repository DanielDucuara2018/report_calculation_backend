from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CurrencyPair:

    symbol: str
    price: Optional[str] = None
    quantity: Optional[float] = None
    creation_date: Optional[datetime] = None
    update_date: Optional[datetime] = None
