from __future__ import annotations

import logging
from typing import Optional, Union

from report_calculation.model import CurrencyPair as ModelCurrencyPair
from report_calculation.schema import CurrencyPair as SchemaCurrencyPair
from report_calculation.validations import is_crypto_binance

logger = logging.getLogger(__name__)

EUR_USDT = "EURUSDT"

investment_euros: float = 15302.52
bank_saving_euros: float = 3620


# Total money on cryptos


def total_crypto_usd() -> float:
    logger.info("Calculating total crypto money in usd")
    total_usd = 0

    for currency in ModelCurrencyPair.get():  # type: ignore
        crypto_currency: SchemaCurrencyPair = is_crypto_binance(currency.symbol)
        if quantity := currency.quantity:
            total_usd += float(crypto_currency.price) * quantity

    total = float("{:.2f}".format(total_usd))
    logger.info("Total crypto money: %f usd", total)
    return total


def total_crypto_euros() -> float:
    logger.info("Calculating total crypto money in euros")
    euro_usdt: SchemaCurrencyPair = is_crypto_binance(EUR_USDT)
    total_euros = float("{:.2f}".format(total_crypto_usd() / float(euro_usdt.price)))
    logger.info("Total crypto money: %f euros", total_euros)
    return total_euros


# Total money (total money on cryptos + bank savings)


def total_usd() -> float:
    logger.info("Calculating total money in usd (total crypto money + bank savings)")
    euro_usdt: SchemaCurrencyPair = is_crypto_binance(EUR_USDT)
    total = float(
        "{:.2f}".format(total_crypto_usd() + bank_saving_euros * float(euro_usdt.price))
    )
    logger.info("Total money: %f usd", total)
    return total


def total_euros() -> float:
    logger.info("Calculating total money in euros (total crypto money + bank savings)")
    total = float("{:.2f}".format(total_crypto_euros() + bank_saving_euros))
    logger.info("Total money: %f euro", total)
    return total


# Total profit (total money on cryptos - investment)


def profit_usd() -> float:
    logger.info("Calculating total profit in usd (total crypto money - investment)")
    euro_usdt: SchemaCurrencyPair = is_crypto_binance(EUR_USDT)
    diff = float(
        "{:.2f}".format(total_crypto_usd() - investment_euros * float(euro_usdt.price))
    )
    logger.info("Total profit: %f usd", diff)
    return diff


def profit_euros() -> float:
    logger.info("Calculating total profit in euros (total crypto money - investment)")
    diff = float("{:.2f}".format(total_crypto_euros() - investment_euros))
    logger.info("Total profit: %f euros", diff)
    return diff


# Total invested money


def invested_usd() -> float:
    logger.info("Calculating total investment in usd")
    euro_usdt: SchemaCurrencyPair = is_crypto_binance(EUR_USDT)
    invested_usd = float("{:.2f}".format(investment_euros * float(euro_usdt.price)))
    logger.info("Investment: %f usd", invested_usd)
    return invested_usd


def invested_euros() -> float:
    logger.info("Calculating total investment in euros")
    investment = float("{:.2f}".format(investment_euros))
    logger.info("Investment: %f euros", investment)
    return investment


# update Crypto


def update(symbol: str, quantity: str) -> ModelCurrencyPair:
    logger.info("Updating %s with value %s", symbol, quantity)
    result = ModelCurrencyPair.get(symbol).update(quantity=float(quantity))  # type: ignore
    logger.info("Result %s", result)
    return result


# get crypto


def read(
    symbol: Optional[str] = None,
) -> Union[ModelCurrencyPair, list[ModelCurrencyPair]]:
    if symbol:
        logger.info("Reading %s data", symbol)
        result = ModelCurrencyPair.get(symbol)
    else:
        logger.info("Reading all data")
        result = ModelCurrencyPair.get()
    logger.info("Result %s", result)
    return result


# create crypto


def create(symbol: str, quantity: str) -> ModelCurrencyPair:
    logger.info("Adding %s with value %s", symbol, quantity)
    is_crypto_binance(symbol)
    result = ModelCurrencyPair(symbol=symbol, quantity=float(quantity)).create()
    logger.info("Added %s", result)
    return result


# delete crypto


def delete(symbol: str) -> ModelCurrencyPair:
    logger.info("Deleting %s data", symbol)
    result = ModelCurrencyPair.get(symbol).delete()  # type: ignore
    logger.info("Deleted %s", result)
    return result
