from __future__ import annotations

import logging
from typing import Optional, Union

from report_calculation.model import Purchase
from report_calculation.schema import PurchaseRequest

logger = logging.getLogger(__name__)

# add purchase


def create(user_id: str, purchase: PurchaseRequest) -> Purchase:
    logger.info("Adding purchase")
    result = Purchase(user_id=user_id, **dict(purchase)).create()
    logger.info("Added purchase with info %s for user %s", purchase, user_id)
    return result


# get purchase


def read(
    user_id: str,
    purchase_id: Optional[str] = None,
) -> Union[list[Purchase], Purchase]:
    if purchase_id:
        logger.info("Reading purchase data of %s from user %s", purchase_id, user_id)
        purchases = Purchase.get(purchase_id=purchase_id, user_id=user_id)
    else:
        logger.info("Reading all data from user %s", user_id)
        purchases = Purchase.find(user_id=user_id)
    return purchases


# update purchasee


def update(
    user_id: str,
    purchase_id: str,
    purchase: PurchaseRequest,
) -> Purchase:
    logger.info("Updating purchase data of %s", purchase_id)
    result = Purchase.get(user_id=user_id, purchase_id=purchase_id).update(**dict(purchase))  # type: ignore
    logger.info("Updated purchase %s of user %s", purchase_id, user_id)
    return result


# delete purchase


def delete(user_id: str, purchase_id: str) -> Purchase:
    logger.info("Deleting purchase %s", purchase_id)
    result = Purchase.get(user_id=user_id, purchase_id=purchase_id).delete()  # type: ignore
    logger.info("Deleted purchase %s of user %s", purchase_id, user_id)
    return result
