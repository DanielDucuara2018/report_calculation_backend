from __future__ import annotations

import logging
from typing import Optional, Union

from report_calculation.model import Telegram as ModelTelegram
from report_calculation.schema import TelegramRequest as SchemaTelegramRequest

logger = logging.getLogger(__name__)

# Add Telegram info


def create(
    user_id: str, telegram_id: str, telegram_info: SchemaTelegramRequest
) -> ModelTelegram:
    logger.info("Adding telegram information for user %s", user_id)
    result = ModelTelegram(
        user_id=user_id, telegram_id=telegram_id, **dict(telegram_info)
    )
    result.run()
    result.create()
    logger.info("Added telegram %s for user %s", telegram_id, user_id)
    return result


# run Telegram bot


def run(user_id: str, telegram_id: str) -> bool:
    return ModelTelegram.get(user_id=user_id, telegram_id=telegram_id).run()


# respawn Telegram bot


def respawn(user_id: str, telegram_id: str) -> bool:
    return ModelTelegram.get(user_id=user_id, telegram_id=telegram_id).respawn()


# stop Telegram bot


def stop(user_id: str, telegram_id: str) -> bool:
    return ModelTelegram.get(user_id=user_id, telegram_id=telegram_id).stop()


# delete Telegram info


def delete(user_id: str, telegram_id: str) -> ModelTelegram:
    logger.info("Deleting telegram info %s for user %s", telegram_id, user_id)
    result = ModelTelegram.get(user_id=user_id, telegram_id=telegram_id).delete()
    logger.info("Deleted telegram %s of user %s", telegram_id, user_id)
    return result


# get Telegram info


def read(
    user_id: str,
    telegram_id: Optional[str] = None,
) -> Union[ModelTelegram, list[ModelTelegram]]:
    if telegram_id:
        logger.info("Reading telegram data %s for user %s", telegram_id, user_id)
        result = ModelTelegram.get(user_id=user_id, telegram_id=telegram_id)
    else:
        logger.info("Reading telegram data for user %s", user_id)
        result = ModelTelegram.find(user_id=user_id)
    logger.info("Found Data for telegram %s of user %s", telegram_id, user_id)
    return result


# update Telegram info


def update(
    user_id: str, telegram_id: str, telegram_info: SchemaTelegramRequest
) -> ModelTelegram:
    logger.info("Updating telegram info for user %s with data %s", user_id, telegram_id)
    result = ModelTelegram.get(user_id=user_id, telegram_id=telegram_id).update(
        **dict(telegram_info)
    )
    logger.info("Updated telegram %s of user", telegram_id, user_id)
    return result
