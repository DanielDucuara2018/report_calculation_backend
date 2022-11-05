from apischema import deserialize
from binance.exceptions import BinanceAPIException
from config import binance_client
from errors import NoSuchCryptoPair

from report_calculation.schema import Currency


def is_crypto_binance(symbol: str):
    try:
        return deserialize(Currency, binance_client.get_symbol_ticker(symbol=symbol))
    except BinanceAPIException as err:
        raise NoSuchCryptoPair(err)
