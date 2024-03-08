from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from sqlalchemy import Column
from sqlalchemy import Enum as SaEnum
from sqlalchemy import ForeignKeyConstraint, String
from sqlalchemy.sql.schema import ForeignKey

from report_calculation.model.base import Base, mapper_registry
from report_calculation.model.resource import Resource


# Enumeration classes
class ExchangeName(str, Enum):
    BINANCE = "binance"
    OKX = "okx"


@mapper_registry.mapped
@dataclass
class Exchange(Base, Resource):

    __tablename__ = "exchange"

    __sa_dataclass_metadata_key__ = "sa"

    exchange_name: str = field(
        metadata={
            "sa": Column(
                SaEnum(ExchangeName, name="enum_exchange_name"), primary_key=True
            )
        }
    )

    api_key: str = field(metadata={"sa": Column(String, nullable=False)})

    secret_key: str = field(metadata={"sa": Column(String, nullable=False)})

    user_id: str = field(
        metadata={"sa": Column(String, ForeignKey("user.user_id"), primary_key=True)}
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["user.user_id"],
            name="exchange_user_id_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
