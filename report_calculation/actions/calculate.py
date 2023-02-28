from __future__ import annotations

import logging
from typing import Optional

from report_calculation.errors import NotUserFound
from report_calculation.model import CurrencyPair as ModelCurrencyPair
from report_calculation.model import User as ModelUser
from report_calculation.utils import async_get_symbol_ticker, async_get_symbol_tickers

logger = logging.getLogger(__name__)

EUR_USDT = "EURUSDT"


# Total money on cryptos


async def total_crypto_usd(user: Optional[ModelUser] = None) -> float:
    logger.info("Calculating total crypto money in usd")

    if not user:
        raise NotUserFound(message="Not user found")

    currency_pairs = await async_get_symbol_tickers(
        ModelCurrencyPair.find(user_id=user.user_id)
    )

    total_usd = sum(
        float(currency.price) * currency.quantity
        for currency in currency_pairs
        if currency.quantity
    )

    total = float("{:.2f}".format(total_usd))
    logger.info("Total crypto money: %f usd", total)
    return total


async def total_crypto_euros(user: Optional[ModelUser] = None) -> float:
    logger.info("Calculating total crypto money in euros")

    total = await total_crypto_usd(user)
    currency_pair = await async_get_symbol_ticker(EUR_USDT)

    total_euros = float("{:.2f}".format(total / float(currency_pair.price)))
    logger.info("Total crypto money: %f euros", total_euros)
    return total_euros


# Total money (total money on cryptos + bank savings)


async def total_usd(user: Optional[ModelUser] = None) -> float:
    logger.info("Calculating total money in usd (total crypto money + bank savings)")

    total = await total_crypto_usd(user)
    currency_pair = await async_get_symbol_ticker(EUR_USDT)

    total_usd = float(
        "{:.2f}".format(total + user.savings_euros * float(currency_pair.price))
    )
    logger.info("Total money: %f usd", total_usd)
    return total_usd


async def total_euros(user: Optional[ModelUser] = None) -> float:
    logger.info("Calculating total money in euros (total crypto money + bank savings)")
    total = await total_crypto_euros(user)
    total_euros = float("{:.2f}".format(total + user.savings_euros))
    logger.info("Total money: %f euro", total_euros)
    return total_euros


# Total profit (total money on cryptos - investment)


async def profit_usd(user: Optional[ModelUser] = None) -> float:
    logger.info("Calculating total profit in usd (total crypto money - investment)")

    total = total_crypto_usd(user)
    currency_pair = await async_get_symbol_ticker(EUR_USDT)

    diff = float(
        "{:.2f}".format(
            await total - user.investment_euros * float(currency_pair.price)
        )
    )
    logger.info("Total profit: %f usd", diff)
    return diff


async def profit_euros(user: Optional[ModelUser] = None) -> float:
    logger.info("Calculating total profit in euros (total crypto money - investment)")
    total = await total_crypto_euros(user)
    diff = float("{:.2f}".format(total - user.investment_euros))
    logger.info("Total profit: %f euros", diff)
    return diff


# Total invested money


async def invested_usd(user: Optional[ModelUser] = None) -> float:
    logger.info("Calculating total investment in usd")

    if not user:
        raise NotUserFound(message="Not user found")

    currency_pair = await async_get_symbol_ticker(EUR_USDT)

    invested_usd = float(
        "{:.2f}".format(user.investment_euros * float(currency_pair.price))
    )
    logger.info("Investment: %f usd", invested_usd)
    return invested_usd


async def invested_euros(user: Optional[ModelUser] = None) -> float:
    logger.info("Calculating total investment in euros")

    if not user:
        raise NotUserFound(message="Not user found")

    investment = float("{:.2f}".format(user.investment_euros))
    logger.info("Investment: %f euros", investment)
    return investment
