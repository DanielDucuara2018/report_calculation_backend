from __future__ import annotations

import logging
from typing import Optional, Union

from report_calculation.binance_client import get_symbol_ticker
from report_calculation.model import CurrencyPair, User

logger = logging.getLogger(__name__)

# create crypto


def create(
    user_id: str,
    symbol: str,
    quantity: Optional[Union[float, str]] = None,
    description: Optional[str] = None,
) -> CurrencyPair:
    logger.info("Adding %s with value %s for user %s", symbol, quantity, user_id)
    user = User.get(user_id=user_id)
    if not (connection := user.active_exchange.sync_connection):
        raise Exception  # TODO no exchange defined, add a first exchange info
    get_symbol_ticker(connection, symbol)
    result = CurrencyPair(
        symbol=symbol,
        quantity=float(quantity) if quantity else float(0),
        user_id=user_id,
        description=description,
    ).create()
    logger.info(
        "Added currency %s with quantity %s for user %s", symbol, quantity, user_id
    )
    return result


# delete crypto


def delete(user_id: str, symbol: str) -> CurrencyPair:
    logger.info("Deleting %s data for user %s", symbol, user_id)
    result = CurrencyPair.get(user_id=user_id, symbol=symbol).delete()  # type: ignore
    logger.info("Deleted currency %s of user %s", symbol, user_id)
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
    logger.info("Found data for symbol %s and user_id %s", user_id, symbol)
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
    logger.info("Updated currency %s for user %s", symbol, user_id)
    return result
