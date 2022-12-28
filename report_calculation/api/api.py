from report_calculation.calculate import create, delete, read, update
from report_calculation.config import app
from report_calculation.model import CurrencyPair as ModelCurrencyPair


# add new crypto in database
@app.post("/currencies/{symbol}")
async def create_currency(symbol: str, quantity: str) -> ModelCurrencyPair:
    return create(symbol, quantity)


# get crypto data
@app.get("/currencies/{symbol}")
async def read_currency(symbol: str) -> ModelCurrencyPair:
    return read(symbol)  # type: ignore


@app.get("/currencies")
async def read_currencies() -> list[ModelCurrencyPair]:
    return read()  # type: ignore


# update crypto data
@app.put("/currencies/{symbol}")
async def update_currency(symbol: str, quantity: str) -> ModelCurrencyPair:
    return update(symbol, quantity)


# delete existing from db
@app.delete("/currencies/{symbol}")
async def delete_currency(symbol: str) -> ModelCurrencyPair:
    return delete(symbol)
