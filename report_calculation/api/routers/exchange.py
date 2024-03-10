from fastapi import APIRouter

from report_calculation.actions.exchange import (
    ExchangeName,
    create,
    delete,
    read,
    update,
)
from report_calculation.schema import ExchangeRequest, ExchangeResponse

router = APIRouter(
    prefix="/exchange",
    tags=["exchange"],
    responses={404: {"description": "Not found"}},
)

## Users
# add new exchange info in database
@router.post("/")
async def add_exchange_info(
    user_id: str, exchange_name: ExchangeName, exchange_info: ExchangeRequest
) -> ExchangeResponse:
    return create(user_id, exchange_name, exchange_info)


# get exchange data
@router.get("/{exchange_name}")
async def read_user(user_id: str, exchange_name: ExchangeName) -> ExchangeResponse:
    return read(user_id, exchange_name)


@router.get("/")
async def read_user(user_id: str) -> list[ExchangeResponse]:
    return read(user_id)


# update exchange info
@router.put("/")
async def update_exchange_info(
    user_id: str, exchange_name: ExchangeName, exchange_info: ExchangeRequest
) -> ExchangeResponse:
    return update(user_id, exchange_name, exchange_info)


# delete existing from db
@router.delete("/")
async def delete_currency(
    user_id: str, exchange_name: ExchangeName
) -> ExchangeResponse:
    return delete(user_id, exchange_name)
