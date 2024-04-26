from typing import Optional

from pydantic import BaseModel


class TelegramRequest(BaseModel):

    token: Optional[str] = None
    description: Optional[str] = None


class TelegramResponse(TelegramRequest):

    telegram_id: Optional[str] = None
