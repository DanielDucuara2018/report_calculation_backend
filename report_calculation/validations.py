from apischema import deserialize
from binance.exceptions import BinanceAPIException
from config import binance_client
from errors import InvalidSymbol

from report_calculation.schema import CurrencyPair


def is_crypto_binance(symbol: str):
    try:
        return deserialize(
            CurrencyPair, binance_client.get_symbol_ticker(symbol=symbol)
        )
    except BinanceAPIException:
        raise InvalidSymbol(
            symbol=symbol, messages=f"Invalid symbol {symbol} in Binance Exchange"
        )
