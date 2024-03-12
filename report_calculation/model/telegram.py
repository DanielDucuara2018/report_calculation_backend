from __future__ import annotations

import logging
import os
import signal
import subprocess
from dataclasses import dataclass, field
from typing import Optional

from sqlalchemy import Column, ForeignKeyConstraint, Integer, String
from sqlalchemy.sql.schema import ForeignKey

from report_calculation.errors import NoTeletramBotProcess, TeletramBotAlreadyRunning
from report_calculation.model.base import Base, mapper_registry
from report_calculation.model.resource import Resource

logger = logging.getLogger(__name__)


@mapper_registry.mapped
@dataclass
class Telegram(Base, Resource):

    __tablename__ = "telegram"

    __sa_dataclass_metadata_key__ = "sa"

    telegram_id: str = field(metadata={"sa": Column(String, primary_key=True)})

    token: str = field(metadata={"sa": Column(String, nullable=False)})

    user_id: str = field(
        metadata={"sa": Column(String, ForeignKey("user.user_id"), primary_key=True)}
    )

    pid: Optional[int] = field(
        metadata={"sa": Column(Integer, default=None, nullable=True)}
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["user.user_id"],
            name="telegram_user_id_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )

    def run(self) -> bool:
        if self.pid:
            logger.info(
                "Telegram bot already running with PID and telegram id %s for user %s",
                self.pid,
                self.telegram_id,
                self.user_id,
            )
            raise TeletramBotAlreadyRunning(
                user_id=self.user_id, telegram_id=self.telegram_id, value=self.pid
            )
        logger.info(
            "Running telegram bot for user %s with telegram id %s.",
            self.user_id,
            self.telegram_id,
        )
        pid = subprocess.Popen(
            [
                "telegram-bot",
                "--telegram-id",
                self.telegram_id,
                "--telegram-token",
                self.token,
            ]
        ).pid
        logger.info("Telegram bot running on PID %s", pid)
        self.update(pid=pid)
        return True

    def stop(self) -> bool:
        if not self.pid:
            logger.info(
                "There is not telegram bot running for telegram id %s for user %s",
                self.telegram_id,
                self.user_id,
            )
            raise NoTeletramBotProcess(
                user_id=self.user_id, telegram_id=self.telegram_id, value=self.pid
            )
        logger.info(
            "Stoping telegram bot process with PID %s for user %s",
            self.pid,
            self.user_id,
        )
        os.kill(self.pid, signal.SIGTERM)
        self.update(force_update=True, pid=None)
        return True
