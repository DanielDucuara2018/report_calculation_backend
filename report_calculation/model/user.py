from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship

from report_calculation.model.base import Base, mapper_registry
from report_calculation.model.purchase import Purchase
from report_calculation.model.resource import Resource
from report_calculation.utils import idv2

if TYPE_CHECKING:
    from report_calculation.model.currency import CurrencyPair


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
        default_factory=float, metadata={"sa": Column(Float, nullable=False)}
    )
    savings_euros: Optional[float] = field(
        default_factory=float, metadata={"sa": Column(Float, nullable=False)}
    )

    # relationships

    # association between User -> CurrencyPair
    currency_pairs: list["CurrencyPair"] = field(
        default_factory=list,
        metadata={"sa": relationship("CurrencyPair")},
    )

    # association between User -> Purchases
    purchases: list["Purchase"] = field(
        default_factory=list,
        metadata={"sa": relationship("Purchase")},
    )
