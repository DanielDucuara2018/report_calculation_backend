from __future__ import annotations

from typing import Any

from config import logger
from validations import is_crypto_binance

from report_calculation.model import Currency as ModelCurrency
from report_calculation.schema import Currency as SchemaCurrency

EUR_USDT = "EURUSDT"

investment_euros: float = 14802.52
bank_saving_euros: float = 3520


# Total money on cryptos


def total_crypto_usd() -> float:
    logger.info("Calculating total crypto money in usd")
    total_usd = 0

    for currency in ModelCurrency.get_all():
        crypto_currency: SchemaCurrency = is_crypto_binance(currency.symbol)
        if quantity := currency.quantity:
            total_usd += float(crypto_currency.price) * quantity

    logger.info(f"Total crypto money: {total_usd} usd")
    return float("{:.2f}".format(total_usd))


def total_crypto_euros() -> float:
    logger.info("Calculating total crypto money in euros")
    euro_usdt: SchemaCurrency = is_crypto_binance(EUR_USDT)
    total_euros = total_crypto_usd() / float(euro_usdt.price)
    logger.info(f"Total crypto money: {total_euros} euros")
    return float("{:.2f}".format(total_euros))


# Total money (total money on cryptos + bank savings)


def total_usd() -> float:
    logger.info("Calculating total money in usd (total crypto money + bank savings)")
    euro_usdt: SchemaCurrency = is_crypto_binance(EUR_USDT)
    total = total_crypto_usd() + bank_saving_euros * float(euro_usdt.price)
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
    euro_usdt: SchemaCurrency = is_crypto_binance(EUR_USDT)
    diff = total_crypto_usd() - investment_euros * float(euro_usdt.price)
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
    euro_usdt: SchemaCurrency = is_crypto_binance(EUR_USDT)
    return float("{:.2f}".format(investment_euros * float(euro_usdt.price)))


def invested_euros() -> float:
    logger.info("Calculating total investment in euros")
    return float("{:.2f}".format(investment_euros))


# update Crypto


def update(symbol: str, quantity: str) -> dict[str, Any]:
    logger.info(f"Updating {symbol} with value {quantity}")
    result = (
        ModelCurrency.get_by_id(symbol).update(quantity=float(quantity))
    ).to_dict()
    logger.info(f"Updated {result}")
    return result


# get crypto


def read(symbol: str) -> dict[str, Any]:
    logger.info(f"Reading {symbol} data")
    result = (ModelCurrency.get_by_id(symbol)).to_dict()
    logger.info(f"Result {result}")
    return result


# create crypto


def create(symbol: str, quantity: str) -> dict[str, Any]:
    logger.info(f"Adding {symbol} with value {quantity}")
    result = (ModelCurrency(symbol=symbol, quantity=float(quantity)).create()).to_dict()
    logger.info(f"Added {result}")
    return result


# delete crypto


def delete(symbol: str) -> dict[str, Any]:
    logger.info(f"Deleting {symbol} data")
    result = (ModelCurrency.get_by_id(symbol).delete()).to_dict()
    logger.info(f"Deleted {result}")
    return result
