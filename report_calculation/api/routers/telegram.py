from enum import Enum

from fastapi import APIRouter

from report_calculation.actions.telegram import create, delete, read, run, stop, update
from report_calculation.schema import TelegramRequest, TelegramResponse

router = APIRouter(
    prefix="/telegram",
    tags=["telegram"],
    responses={404: {"description": "Not found"}},
)


class TelegramBotActions(str, Enum):
    RUN = "run"
    STOP = "stop"


telegram_bot_actions = {
    TelegramBotActions.RUN: run,
    TelegramBotActions.STOP: stop,
}

## Telegram
# add new telegram info in database
@router.post("/")
async def add_telegram_info(
    user_id: str, telegram_id: str, telegram_info: TelegramRequest
) -> TelegramResponse:
    return create(user_id, telegram_id, telegram_info)


# run or stop telegram bot
@router.post("/{telegram_id}/{action}")
async def run_telegram_bot(
    user_id: str, telegram_id: str, action: TelegramBotActions
) -> bool:
    return telegram_bot_actions.get(action)(user_id, telegram_id)


# get telegram info
@router.get("/{telegram_id}")
async def read_user(user_id: str, telegram_id: str) -> TelegramResponse:
    return read(user_id, telegram_id)


@router.get("/")
async def read_user(user_id: str) -> list[TelegramResponse]:
    return read(user_id)


# update telegram info
@router.put("/")
async def update_user(
    user_id: str, telegram_id: str, telegram_info: TelegramRequest
) -> TelegramResponse:
    return update(user_id, telegram_id, telegram_info)


# delete telegram info
@router.delete("/")
async def delete_currency(user_id: str, telegram_id: str) -> TelegramResponse:
    return delete(user_id, telegram_id)
