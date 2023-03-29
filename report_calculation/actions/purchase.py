from __future__ import annotations

import logging
from typing import Optional

from report_calculation.model import Purchase
from report_calculation.schema import PurchaseRequest

logger = logging.getLogger(__name__)

# add purchase


def create(purchase: PurchaseRequest) -> Purchase:
    logger.info("Adding purchase")
    result = Purchase(**dict(purchase)).create()
    logger.info("Added %s", result)
    return result


# get purchase


def read(
    user_id: str,
    purchase_id: Optional[str] = None,
) -> list[Purchase]:
    if purchase_id:
        logger.info("Reading purchase data of %s from user %s", purchase_id, user_id)
        result = Purchase.find(purchase_id=purchase_id, user_id=user_id)
    else:
        logger.info("Reading all data from user %s", user_id)
        result = Purchase.find(user_id=user_id)
    return result


# update purchase


def update(
    purchase_id: str,
    purchase: PurchaseRequest,
) -> Purchase:
    logger.info("Updating purchase data of %s", purchase_id)
    result = Purchase.get(purchase_id=purchase_id).update(**dict(purchase))  # type: ignore
    logger.info("Result %s", result)
    return result


# delete purchase


def delete(purchase_id: str) -> Purchase:
    logger.info("Deleting purchase %s", purchase_id)
    result = Purchase.get(purchase_id=purchase_id).delete()  # type: ignore
    logger.info("Deleted %s", result)
    return result
