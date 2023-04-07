from typing import Optional, Union

from fastapi import APIRouter

from report_calculation.actions.currency import create, delete, read, update
from report_calculation.schema import CurrencyPairRequest, CurrencyPairResponse

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
    user_id: str, symbol: str, data: CurrencyPairRequest
) -> CurrencyPairResponse:
    return create(user_id, symbol, data.quantity, data.description)


# get crypto data
@router.get("/")
async def read_currency(
    user_id: str, symbol: Optional[str] = None
) -> Union[list[CurrencyPairResponse], CurrencyPairResponse]:
    if symbol:
        return read(user_id, symbol)
    return read(user_id)


# update crypto data
@router.put("/")
async def update_currency(
    user_id: str, symbol: str, data: CurrencyPairRequest
) -> CurrencyPairResponse:
    return update(user_id, symbol, data.quantity, data.description)


# delete existing from db
@router.delete("/")
async def delete_currency(user_id: str, symbol: str) -> CurrencyPairResponse:
    return delete(user_id, symbol)
