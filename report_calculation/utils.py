import asyncio
import logging
from typing import Any, Callable, Optional

from apischema import deserialize
from binance import AsyncClient
from binance.exceptions import BinanceAPIException

from report_calculation.config import binance_client, init_binance_connection_async
from report_calculation.errors import InvalidSymbol
from report_calculation.model import CurrencyPair as ModelCurrencyPair
from report_calculation.schema import CurrencyPairResponse as SchemaCurrencyPairResponse

logger = logging.getLogger(__name__)


async def async_get_symbol_tickers(currencies: list[ModelCurrencyPair]):
    client: AsyncClient = await init_binance_connection_async()
    currency_pairs: list[SchemaCurrencyPairResponse] = await asyncio.gather(
        *(
            _async_execute_binance_function(
                client.get_symbol_ticker, currency.symbol, quantity=currency.quantity
            )
            for currency in currencies
        )
    )
    await client.close_connection()
    return currency_pairs


async def async_get_symbol_ticker(symbol: str):
    client: AsyncClient = await init_binance_connection_async()
    currency_pair: SchemaCurrencyPairResponse = await _async_execute_binance_function(
        client.get_symbol_ticker, symbol
    )
    await client.close_connection()
    return currency_pair


def get_symbol_ticker(symbol: str):
    return _execute_binance_function(binance_client.get_symbol_ticker, symbol)


def _execute_binance_function(
    func: Callable[[Any], Any], symbol: str
) -> SchemaCurrencyPairResponse:
    try:
        return deserialize(SchemaCurrencyPairResponse, func(symbol=symbol))
    except BinanceAPIException:
        logger.error("Invalid symbol %s in Binance Exchange", symbol)
        raise InvalidSymbol(
            symbol=symbol, messages=f"Invalid symbol {symbol} in Binance Exchange"
        )


async def _async_execute_binance_function(
    func: Callable[[Any], Any], symbol: str, *, quantity: Optional[float] = None
) -> SchemaCurrencyPairResponse:
    try:
        currency_pair: SchemaCurrencyPairResponse = deserialize(
            SchemaCurrencyPairResponse,
            await func(symbol=symbol),
        )
        currency_pair.quantity = quantity
        return currency_pair
    except BinanceAPIException:
        logger.error("Invalid symbol %s in Binance Exchange", symbol)
        raise InvalidSymbol(
            symbol=symbol, messages=f"Invalid symbol {symbol} in Binance Exchange"
        )
