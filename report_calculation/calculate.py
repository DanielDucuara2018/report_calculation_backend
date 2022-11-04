from __future__ import annotations
from typing import Any

from config import binance_client, logger
from apischema import deserialize
from binance.exceptions import BinanceAPIException
from dataclasses import dataclass

from report_calculation.model import Currency

EUR_USDT="EURUSDT"
 
investment_euros: float = 14802.52
bank_saving_euros: float = 3520

@dataclass
class CryptoCurrency:

    symbol: str 
    price: str 

# Total money on cryptos

def total_crypto_usd() -> float:
    logger.info("Calculating total crypto money in usd")
    total_usd = 0

    for currency in Currency.get_all():
        try:
            crypto_currency: CryptoCurrency = deserialize(CryptoCurrency, binance_client.get_symbol_ticker(symbol=currency.symbol))
            if quantity := currency.quantity:
                total_usd += float(crypto_currency.price)*quantity
        except BinanceAPIException as err:
            logger.exception(f"Error {err} {currency.symbol}")
            raise
    logger.info(f"Total crypto money: {total_usd} usd")
    return float("{:.2f}".format(total_usd)) 


def total_crypto_euros() -> float:
    logger.info("Calculating total crypto money in euros")
    euro_usdt : CryptoCurrency = deserialize(CryptoCurrency, binance_client.get_symbol_ticker(symbol=EUR_USDT))
    total_euros = total_crypto_usd()/float(euro_usdt.price)
    logger.info(f"Total crypto money: {total_euros} euros") 
    return float("{:.2f}".format(total_euros))

# Total money (total money on cryptos + bank savings)

def total_usd() -> float:
    logger.info("Calculating total money in usd (total crypto money + bank savings)")
    euro_usdt : CryptoCurrency = deserialize(CryptoCurrency, binance_client.get_symbol_ticker(symbol=EUR_USDT))
    total = total_crypto_usd() + bank_saving_euros*float(euro_usdt.price)
    logger.info(f"Total money: {total} usd")
    return float("{:.2f}".format(total))


def total_euros() -> float:
    logger.info("Calculating total money in euros (total crypto money + bank savings)")
    total = total_crypto_euros() + bank_saving_euros
    logger.info(f"Total money: {total} euro")
    return float("{:.2f}".format(total))

# Total profit (total money on cryptos - investment)

def profit_usd() -> float:
    logger.info("Calculating total profit in usd (total crypto money - investment)")
    euro_usdt : CryptoCurrency = deserialize(CryptoCurrency, binance_client.get_symbol_ticker(symbol=EUR_USDT))
    diff = total_crypto_usd() - investment_euros*float(euro_usdt.price)
    logger.info(f"Total profit: {diff} usd")
    return float("{:.2f}".format(diff))


def profit_euros() -> float:
    logger.info("Calculating total profit in euros (total crypto money - investment)")
    diff = total_crypto_euros() - investment_euros
    logger.info(f"Total profit: {diff} euros")
    return float("{:.2f}".format(diff))

# Total invested money

def invested_usd() -> float:
    logger.info("Calculating total investment in usd")
    euro_usdt : CryptoCurrency = deserialize(CryptoCurrency, binance_client.get_symbol_ticker(symbol=EUR_USDT))
    return float("{:.2f}".format(investment_euros*float(euro_usdt.price)))

def invested_euros() -> float:
    logger.info("Calculating total investment in euros")
    return float("{:.2f}".format(investment_euros))

# update Crypto

def update(symbol: str, quantity: str) -> dict[str, Any]:
    logger.info(f"Updating {symbol} with value {quantity}")
    result = (Currency.get_by_id(symbol).update(quantity=float(quantity))).to_dict()
    logger.info(f"Updated {result}")
    return result

# get crypto

def read(symbol:str) -> dict[str, Any]:
    logger.info(f"Reading {symbol} data")
    result = (Currency.get_by_id(symbol)).to_dict()
    logger.info(f"Result {result}")
    return result

# create crypto

def create(symbol: str, quantity: str) -> dict[str, Any]:
    logger.info(f"Adding {symbol} with value {quantity}")
    result = (Currency(symbol=symbol, quantity=float(quantity)).create()).to_dict()
    logger.info(f"Added {result}")
    return result

# delete crypto 

def delete(symbol: str) -> dict[str, Any]:
    logger.info(f"Deleting {symbol} data")
    result = (Currency.get_by_id(symbol).delete()).to_dict()
    logger.info(f"Deleted {result}")
    return result



