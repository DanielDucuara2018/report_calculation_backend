from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship

from report_calculation.model.base import Base, mapper_registry
from report_calculation.model.resource import Resource

if TYPE_CHECKING:
    from report_calculation.model.currency import CurrencyPair


def idv2(prefix: str, *, version: int = 0) -> str:  # fix calculation
    random_bytes = (version << 127) + random.getrandbits(32)
    return f"{prefix}-{random_bytes:032x}"


@mapper_registry.mapped
@dataclass
class User(Base, Resource):

    __tablename__ = "user"

    __sa_dataclass_metadata_key__ = "sa"

    user_id: str = field(
        init=False,
        metadata={
            "sa": Column(
                String, default=lambda: idv2("user", version=1), primary_key=True
            )
        },
    )
    telegram_id: Optional[str] = field(
        metadata={"sa": Column(String, nullable=False)}
    )  # TODO this value can be shared among users ?
    investment_euros: Optional[float] = field(
        metadata={"sa": Column(Float, default=float(0), nullable=False)}
    )
    savings_euros: Optional[float] = field(
        metadata={"sa": Column(Float, default=float(0), nullable=False)}
    )

    # relationships

    # association between User -> CurrencyPair
    currency_pairs: list["CurrencyPair"] = field(
        default_factory=list,
        metadata={"sa": relationship("CurrencyPair")},
    )
