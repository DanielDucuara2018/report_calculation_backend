from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from report_calculation.model.base import Base, mapper_registry
from report_calculation.model.purchase import Purchase
from report_calculation.model.resource import Resource


@mapper_registry.mapped
@dataclass
class CurrencyPair(Base, Resource):

    __tablename__ = "currency_pair"

    __sa_dataclass_metadata_key__ = "sa"

    # primary key

    symbol: str = field(metadata={"sa": Column(String, primary_key=True)})

    # foreign key

    user_id: str = field(
        metadata={"sa": Column(String, ForeignKey("user.user_id"), primary_key=True)}
    )

    # attributes

    quantity: Optional[float] = field(
        metadata={"sa": Column(Float, default=float(0), nullable=False)}
    )

    # relationships

    # association between Purchases -> Purchases
    purchases: list["Purchase"] = field(
        default_factory=list,
        metadata={"sa": relationship("Purchase")},
    )

    def __str__(self) -> str:
        return f"Pair {self.symbol} with {self.quantity} tokens"
