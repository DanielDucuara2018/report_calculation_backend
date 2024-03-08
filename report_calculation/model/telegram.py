from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import Column, ForeignKeyConstraint, String
from sqlalchemy.sql.schema import ForeignKey

from report_calculation.model.base import Base, mapper_registry
from report_calculation.model.resource import Resource


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

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["user.user_id"],
            name="telegram_user_id_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
