from __future__ import annotations

import logging

from report_calculation.model import CurrencyPair as ModelCurrencyPair
from report_calculation.model import User as ModelUser
from report_calculation.utils import async_get_symbol_ticker, async_get_symbol_tickers

logger = logging.getLogger(__name__)

EUR_USDT = "EURUSDT"

investment_euros: float = 16802.52
bank_saving_euros: float = 2520


# Total money on cryptos


async def total_crypto_usd() -> float:
    logger.info("Calculating total crypto money in usd")

    currency_pairs = await async_get_symbol_tickers(ModelCurrencyPair.get())

    total_usd = sum(
        float(currency.price) * currency.quantity
        for currency in currency_pairs
        if currency.quantity
    )

    total = float("{:.2f}".format(total_usd))
    logger.info("Total crypto money: %f usd", total)
    return total


async def total_crypto_euros() -> float:
    logger.info("Calculating total crypto money in euros")

    currency_pair = await async_get_symbol_ticker(EUR_USDT)

    total_euros = float(
        "{:.2f}".format(await total_crypto_usd() / float(currency_pair.price))
    )
    logger.info("Total crypto money: %f euros", total_euros)
    return total_euros


# Total money (total money on cryptos + bank savings)


async def total_usd() -> float:
    logger.info("Calculating total money in usd (total crypto money + bank savings)")

    currency_pair = await async_get_symbol_ticker(EUR_USDT)

    total = float(
        "{:.2f}".format(
            await total_crypto_usd() + bank_saving_euros * float(currency_pair.price)
        )
    )
    logger.info("Total money: %f usd", total)
    return total


async def total_euros() -> float:
    logger.info("Calculating total money in euros (total crypto money + bank savings)")
    total = float("{:.2f}".format(await total_crypto_euros() + bank_saving_euros))
    logger.info("Total money: %f euro", total)
    return total


# Total profit (total money on cryptos - investment)


async def profit_usd() -> float:
    logger.info("Calculating total profit in usd (total crypto money - investment)")

    currency_pair = await async_get_symbol_ticker(EUR_USDT)

    diff = float(
        "{:.2f}".format(
            await total_crypto_usd() - investment_euros * float(currency_pair.price)
        )
    )
    logger.info("Total profit: %f usd", diff)
    return diff


async def profit_euros() -> float:
    logger.info("Calculating total profit in euros (total crypto money - investment)")
    diff = float("{:.2f}".format(await total_crypto_euros() - investment_euros))
    logger.info("Total profit: %f euros", diff)
    return diff


# Total invested money


async def invested_usd() -> float:
    logger.info("Calculating total investment in usd")

    currency_pair = await async_get_symbol_ticker(EUR_USDT)

    invested_usd = float("{:.2f}".format(investment_euros * float(currency_pair.price)))
    logger.info("Investment: %f usd", invested_usd)
    return invested_usd


async def invested_euros() -> float:
    logger.info("Calculating total investment in euros")
    investment = float("{:.2f}".format(investment_euros))
    logger.info("Investment: %f euros", investment)
    return investment
