from fastapi import APIRouter, Depends

from report_calculation.actions.exchange import (
    ExchangeName,
    create,
    delete,
    read,
    update,
)
from report_calculation.actions.user import get_current_user
from report_calculation.schema import ExchangeRequest, ExchangeResponse, UserResponse

router = APIRouter(
    prefix="/exchange",
    tags=["exchange"],
    responses={404: {"description": "Not found"}},
)

## Users
# add new exchange info in database
@router.post("/")
async def add_exchange_info(
    exchange_name: ExchangeName,
    exchange_info: ExchangeRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> ExchangeResponse:
    return create(current_user.user_id, exchange_name, exchange_info)


# get exchange data
@router.get("/{exchange_name}")
async def read_exchange(
    exchange_name: ExchangeName, current_user: UserResponse = Depends(get_current_user)
) -> ExchangeResponse:
    return read(current_user.user_id, exchange_name)


@router.get("/")
async def read_exchanges(
    current_user: UserResponse = Depends(get_current_user),
) -> list[ExchangeResponse]:
    return read(current_user.user_id)


# update exchange info
@router.put("/")
async def update_exchange_info(
    exchange_name: ExchangeName,
    exchange_info: ExchangeRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> ExchangeResponse:
    return update(current_user.user_id, exchange_name, exchange_info)


# delete existing from db
@router.delete("/")
async def delete_currency(
    exchange_name: ExchangeName, current_user: UserResponse = Depends(get_current_user)
) -> ExchangeResponse:
    return delete(current_user.user_id, exchange_name)
