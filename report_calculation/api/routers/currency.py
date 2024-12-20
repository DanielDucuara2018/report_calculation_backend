from dataclasses import asdict
from typing import Optional, Union

from fastapi import APIRouter, Depends

from report_calculation.actions.currency import create, delete, read, update
from report_calculation.actions.user import get_current_user
from report_calculation.model import User
from report_calculation.schema import (
    CurrencyPairRequest,
    CurrencyPairResponse,
    UserResponse,
)

router = APIRouter(
    prefix="/currencies",
    tags=["currencies"],
    responses={404: {"description": "Not found"}},
)

# TODO check if all methods can use CurrencyPairEntry


## Currencies
# add new crypto in database
@router.post("/")
async def create_currency(
    symbol: str,
    data: CurrencyPairRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> CurrencyPairResponse:
    return create(current_user.user_id, symbol, data.quantity, data.description)


# get crypto data
@router.get("/")
async def read_currency(
    symbol: Optional[str] = None, current_user: UserResponse = Depends(get_current_user)
) -> Union[list[CurrencyPairResponse], CurrencyPairResponse]:
    user_id = current_user.user_id
    exchange_connection = User.get(user_id=user_id).active_exchange.sync_connection
    if symbol:
        currency = read(user_id, symbol)
        return CurrencyPairResponse(
            price=currency.price(exchange_connection), **asdict(read(user_id, symbol))
        )
    currencies = read(user_id)
    return [
        CurrencyPairResponse(
            price=currency.price(exchange_connection), **asdict(currency)
        )
        for currency in currencies
    ]


# update crypto data
@router.put("/")
async def update_currency(
    symbol: str,
    data: CurrencyPairRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> CurrencyPairResponse:
    return update(current_user.user_id, symbol, data.quantity, data.description)


# delete existing from db
@router.delete("/")
async def delete_currency(
    symbol: str, current_user: UserResponse = Depends(get_current_user)
) -> CurrencyPairResponse:
    return delete(current_user.user_id, symbol)
