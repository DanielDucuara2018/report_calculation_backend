from __future__ import annotations

import logging
from typing import Optional, Union

from report_calculation.model import User as ModelUser
from report_calculation.schema import User as SchemaUser

logger = logging.getLogger(__name__)

# create User


def create(user: SchemaUser) -> ModelUser:
    logger.info("Adding new user")
    result = ModelUser(**dict(user)).create()
    logger.info("Added %s", result)
    return result


# delete User


def delete(user_id: str) -> ModelUser:
    logger.info("Deleting %s user", user_id)
    result = ModelUser.get(user_id).delete()
    logger.info("Deleted %s", result)
    return result


# get User


def read(
    user_id: Optional[str] = None,
) -> Union[ModelUser, list[ModelUser]]:
    if user_id:
        logger.info("Reading %s data", user_id)
        result = ModelUser.get(user_id)
    else:
        logger.info("Reading all data")
        result = ModelUser.get()
    logger.info("Result %s", result)
    return result


# update User


def update(user_id: str, data: SchemaUser) -> ModelUser:
    logger.info("Updating %s with data %s", user_id, data)
    result = ModelUser.get(user_id).update(**dict(data))
    logger.info("Result %s", result)
    return result
