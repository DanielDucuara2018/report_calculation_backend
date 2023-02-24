from __future__ import annotations

import logging
from typing import Optional, Union

from report_calculation.model import CurrencyPair as ModelCurrencyPair
from report_calculation.utils import get_symbol_ticker

logger = logging.getLogger(__name__)

# create crypto


def create(symbol: str, quantity: str) -> ModelCurrencyPair:
    logger.info("Adding %s with value %s", symbol, quantity)
    get_symbol_ticker(symbol)
    result = ModelCurrencyPair(symbol=symbol, quantity=float(quantity)).create()
    logger.info("Added %s", result)
    return result


# delete crypto


def delete(symbol: str) -> ModelCurrencyPair:
    logger.info("Deleting %s data", symbol)
    result = ModelCurrencyPair.get(symbol).delete()  # type: ignore
    logger.info("Deleted %s", result)
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


# update Crypto


def update(symbol: str, quantity: str) -> ModelCurrencyPair:
    logger.info("Updating %s with value %s", symbol, quantity)
    result = ModelCurrencyPair.get(symbol).update(quantity=float(quantity))  # type: ignore
    logger.info("Result %s", result)
    return result
