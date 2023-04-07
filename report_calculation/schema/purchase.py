from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PurchaseRequest(BaseModel):

    user_id: Optional[str] = None
    symbol: Optional[str] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    date: Optional[datetime] = None
    description: Optional[str] = None


class PurchaseResponse(PurchaseRequest):

    purchase_id: Optional[str] = None
    gain: Optional[float] = None
    update_date: Optional[datetime] = None
    creation_date: Optional[datetime] = None
