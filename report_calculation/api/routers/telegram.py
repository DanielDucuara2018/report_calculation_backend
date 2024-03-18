from enum import Enum

from fastapi import APIRouter, Depends

from report_calculation.actions.telegram import create, delete, read, run, stop, update
from report_calculation.actions.user import get_current_user
from report_calculation.schema import TelegramRequest, TelegramResponse, UserResponse

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
    telegram_id: str,
    telegram_info: TelegramRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> TelegramResponse:
    return create(current_user.user_id, telegram_id, telegram_info)


# run or stop telegram bot
@router.post("/{telegram_id}/{action}")
async def run_telegram_bot(
    telegram_id: str,
    action: TelegramBotActions,
    current_user: UserResponse = Depends(get_current_user),
) -> bool:
    return telegram_bot_actions.get(action)(current_user.user_id, telegram_id)


# get telegram info
@router.get("/{telegram_id}")
async def read_telegram_bot(
    telegram_id: str, current_user: UserResponse = Depends(get_current_user)
) -> TelegramResponse:
    return read(current_user.user_id, telegram_id)


@router.get("/")
async def read_telegram_bots(
    current_user: UserResponse = Depends(get_current_user),
) -> list[TelegramResponse]:
    return read(current_user.user_id)


# update telegram info
@router.put("/")
async def update_telegram(
    telegram_id: str,
    telegram_info: TelegramRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> TelegramResponse:
    return update(current_user.user_id, telegram_id, telegram_info)


# delete telegram info
@router.delete("/")
async def delete_telegram(
    telegram_id: str, current_user: UserResponse = Depends(get_current_user)
) -> TelegramResponse:
    return delete(current_user.user_id, telegram_id)
