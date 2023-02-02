from report_calculation.calculate import create, delete, read, update
from report_calculation.config import app
from report_calculation.schema import CurrencyPair as SchemaCurrencyPair


@app.get("/")
async def root():
    return {"message": "Welcome to report_calculation app"}


## Currencies
# add new crypto in database
@app.post("/currencies/{symbol}")
async def create_currency(symbol: str, quantity: str) -> SchemaCurrencyPair:
    return create(symbol, quantity)


# get crypto data
@app.get("/currencies/{symbol}")
async def read_currency(symbol: str) -> SchemaCurrencyPair:
    return read(symbol)  # type: ignore


@app.get("/currencies")
async def read_currencies() -> list[SchemaCurrencyPair]:
    return read()  # type: ignore


# update crypto data
@app.put("/currencies/{symbol}")
async def update_currency(symbol: str, quantity: str) -> SchemaCurrencyPair:
    return update(symbol, quantity)


# delete existing from db
@app.delete("/currencies/{symbol}")
async def delete_currency(symbol: str) -> SchemaCurrencyPair:
    return delete(symbol)


## Calculate


@app.get("calculate/{method}")
async def calculate(method: str):
    pass
