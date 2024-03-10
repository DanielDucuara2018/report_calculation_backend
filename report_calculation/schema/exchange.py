from typing import Optional

from pydantic import BaseModel


class ExchangeRequest(BaseModel):

    api_key: Optional[str] = None
    secret_key: Optional[str] = None
    description: Optional[str] = None


class ExchangeResponse(ExchangeRequest):

    user_id: Optional[str] = None
    exchange_name: Optional[str] = None
