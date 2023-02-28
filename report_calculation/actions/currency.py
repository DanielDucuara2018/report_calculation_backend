from __future__ import annotations

import logging
from typing import Optional, Union

from report_calculation.model import CurrencyPair as ModelCurrencyPair
from report_calculation.utils import get_symbol_ticker

logger = logging.getLogger(__name__)

# create crypto


def create(
    user_id: str, symbol: str, quantity: Optional[Union[str, float]] = None
) -> ModelCurrencyPair:
    logger.info("Adding %s with value %s for user %s", symbol, quantity, user_id)
    get_symbol_ticker(symbol)
    result = ModelCurrencyPair(
        symbol=symbol, quantity=float(quantity or str(0)), user_id=user_id
    ).create()
    logger.info("Added %s", result)
    return result


# delete crypto


def delete(user_id: str, symbol: str) -> ModelCurrencyPair:
    logger.info("Deleting %s data for user %s", symbol, user_id)
    result = ModelCurrencyPair.get(user_id=user_id, symbol=symbol).delete()  # type: ignore
    logger.info("Deleted %s", result)
    return result


# get crypto


def read(
    user_id: str,
    symbol: Optional[str] = None,
) -> Union[ModelCurrencyPair, list[ModelCurrencyPair]]:
    if symbol:
        logger.info("Reading %s data for user %s", symbol, user_id)
        result = ModelCurrencyPair.get(user_id=user_id, symbol=symbol)
    else:
        logger.info("Reading all data for user %s", user_id)
        result = ModelCurrencyPair.find(user_id=user_id)
    logger.info("Result %s", result)
    return result


# update Crypto


def update(
    user_id: str, symbol: str, quantity: Optional[float] = None
) -> ModelCurrencyPair:
    logger.info("Updating %s with value %s for user %s", symbol, quantity, user_id)
    result = ModelCurrencyPair.get(user_id=user_id, symbol=symbol).update(quantity=float(quantity or str(0)))  # type: ignore
    logger.info("Result %s", result)
    return result
