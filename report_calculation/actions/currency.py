from __future__ import annotations

import logging
from typing import Optional, Union

from report_calculation.binance_client import get_symbol_ticker
from report_calculation.model import CurrencyPair

logger = logging.getLogger(__name__)

# create crypto


def create(
    user_id: str,
    symbol: str,
    quantity: Optional[Union[float, str]] = None,
    description: Optional[str] = None,
) -> CurrencyPair:
    logger.info("Adding %s with value %s for user %s", symbol, quantity, user_id)
    get_symbol_ticker(symbol)
    result = CurrencyPair(
        symbol=symbol,
        quantity=float(quantity) if quantity else float(0),
        user_id=user_id,
        description=description,
    ).create()
    logger.info("Added %s", result)
    return result


# delete crypto


def delete(user_id: str, symbol: str) -> CurrencyPair:
    logger.info("Deleting %s data for user %s", symbol, user_id)
    result = CurrencyPair.get(user_id=user_id, symbol=symbol).delete()  # type: ignore
    logger.info("Deleted %s", result)
    return result


# get crypto


def read(
    user_id: str,
    symbol: Optional[str] = None,
) -> Union[CurrencyPair, list[CurrencyPair]]:
    if symbol:
        logger.info("Reading %s data for user %s", symbol, user_id)
        result = CurrencyPair.get(user_id=user_id, symbol=symbol)
    else:
        logger.info("Reading all data for user %s", user_id)
        result = CurrencyPair.find(user_id=user_id)
    logger.info("Result %s", result)
    return result


# update Crypto


def update(
    user_id: str,
    symbol: str,
    quantity: Optional[Union[float, str]] = None,
    description: Optional[str] = None,
) -> CurrencyPair:
    logger.info("Updating %s with value %s for user %s", symbol, quantity, user_id)
    result = CurrencyPair.get(user_id=user_id, symbol=symbol)
    result.update(quantity=float(quantity) if quantity else result.quantity, description=description)  # type: ignore
    logger.info("Result %s", result)
    return result
