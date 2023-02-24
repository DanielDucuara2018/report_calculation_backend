from fastapi import APIRouter

from report_calculation.actions.currency import create, delete, read, update
from report_calculation.schema import CurrencyPair as SchemaCurrencyPair

router = APIRouter(
    prefix="/currencies",
    tags=["currencies"],
    responses={404: {"description": "Not found"}},
)


## Currencies
# add new crypto in database
@router.post("/{symbol}")
async def create_currency(symbol: str, quantity: str) -> SchemaCurrencyPair:
    return create(symbol, quantity)


# get crypto data
@router.get("/{symbol}")
async def read_currency(symbol: str) -> SchemaCurrencyPair:
    return read(symbol)  # type: ignore


@router.get("/")
async def read_currencies() -> list[SchemaCurrencyPair]:
    return read()  # type: ignore


# update crypto data
@router.put("/{symbol}")
async def update_currency(symbol: str, quantity: str) -> SchemaCurrencyPair:
    return update(symbol, quantity)


# delete existing from db
@router.delete("/{symbol}")
async def delete_currency(symbol: str) -> SchemaCurrencyPair:
    return delete(symbol)
