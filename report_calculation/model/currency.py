from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from sqlalchemy import Column, Float, ForeignKeyConstraint, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from report_calculation.binance_client import get_symbol_ticker
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
        metadata={"sa": Column(String, ForeignKey("account.user_id"), primary_key=True)}
    )

    # attributes

    quantity: Optional[float] = field(
        default_factory=float, metadata={"sa": Column(Float, nullable=False)}
    )

    # relationships

    # association between CurrencyPair -> Purchases
    purchases: list["Purchase"] = field(
        default_factory=list,
        metadata={"sa": relationship("Purchase")},
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["account.user_id"],
            name="currency_pair_user_id_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )

    def price(self, client: Optional[Any] = None) -> float:  # TODO find client typing
        if not client:
            raise Exception  # TODO no exchange defined, add a first exchange info
        return get_symbol_ticker(client, self.symbol).price

    def __str__(self) -> str:
        return f"Pair {self.symbol} with {self.quantity} tokens"
