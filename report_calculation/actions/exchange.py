from __future__ import annotations

import logging
from typing import Optional, Union

from report_calculation.model import Exchange as ModelExchange
from report_calculation.model import ExchangeName
from report_calculation.schema import ExchangeRequest as SchemaExchangeRequest

logger = logging.getLogger(__name__)

# Add exchange info


def create(
    user_id: str, exchange_name: ExchangeName, exchange_info: SchemaExchangeRequest
) -> ModelExchange:
    logger.info("Adding exchange information for user %s", user_id)
    result = ModelExchange(
        user_id=user_id, exchange_name=exchange_name, **dict(exchange_info)
    ).create()
    logger.info("Added exchange %s for user %s", exchange_name, user_id)
    return result


# delete exchange info


def delete(user_id: str, exchange_name: ExchangeName) -> ModelExchange:
    logger.info("Deleting exchange %s for user %s", exchange_name, user_id)
    result = ModelExchange.get(user_id=user_id).delete()
    logger.info("Deleted exchange %s for user %s", exchange_name, user_id)
    return result


# get exchange info


def read(
    user_id: str,
    exchange_name: Optional[ExchangeName] = None,
) -> Union[ModelExchange, list[ModelExchange]]:
    if exchange_name:
        logger.info("Reading %s data of exchange", exchange_name)
        result = ModelExchange.get(user_id=user_id, exchange_name=exchange_name)
    else:
        logger.info("Reading exchange data of user %s", user_id)
        result = ModelExchange.find(user_id=user_id)
    logger.info("Data found for exchange %s for user %s", exchange_name, user_id)
    return result


# update exchange info


def update(
    user_id: str, exchange_name: ExchangeName, exchange_info: SchemaExchangeRequest
) -> ModelExchange:
    logger.info(
        "Updating exchange info for %s for user %s with data %s",
        exchange_name,
        user_id,
        exchange_info,
    )
    result = ModelExchange.get(user_id=user_id, exchange_name=exchange_name).update(
        **dict(exchange_info)
    )
    logger.info("Updated exchange %s of user %s", exchange_name, user_id)
    return result
