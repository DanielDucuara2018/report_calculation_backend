from __future__ import annotations

from config import logger
from validations import is_crypto_binance

from report_calculation.model import CurrencyPair as ModelCurrencyPair
from report_calculation.schema import CurrencyPair as SchemaCurrencyPair

EUR_USDT = "EURUSDT"

investment_euros: float = 14802.52
bank_saving_euros: float = 3520


# Total money on cryptos


def total_crypto_usd() -> float:
    logger.info("Calculating total crypto money in usd")
    total_usd = 0

    for currency in ModelCurrencyPair.get_all():
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


def update(symbol: str, quantity: str) -> str:
    logger.info("Updating %s with value %s", symbol, quantity)
    result = ModelCurrencyPair.get_by_id(symbol).update(quantity=float(quantity))
    logger.info("Result %s", result)
    return f"{result}"


# get crypto


def read(symbol: str) -> str:
    logger.info("Reading %s data", symbol)
    result = ModelCurrencyPair.get_by_id(symbol)
    logger.info("Result %s", result)
    return f"{result}"


# create crypto


def create(symbol: str, quantity: str) -> str:
    logger.info("Adding %s with value %s", symbol, quantity)
    crypto_currency: SchemaCurrencyPair = is_crypto_binance(symbol)
    result = ModelCurrencyPair(symbol=symbol, quantity=float(quantity)).create()
    logger.info("Added %s", result)
    return f"{result}. Total usd {float(crypto_currency.price) * float(quantity)}"


# delete crypto


def delete(symbol: str) -> str:
    logger.info("Deleting %s data", symbol)
    result = ModelCurrencyPair.get_by_id(symbol).delete()
    logger.info("Deleted %s", result)
    return f"{result}"
