from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Float, ForeignKeyConstraint, String
from sqlalchemy.sql.schema import ForeignKey

from report_calculation.binance_client import get_symbol_ticker
from report_calculation.model.base import Base, mapper_registry
from report_calculation.model.resource import Resource
from report_calculation.utils import idv2


@mapper_registry.mapped
@dataclass
class Purchase(Base, Resource):

    __tablename__ = "purchase"

    __sa_dataclass_metadata_key__ = "sa"

    purchase_id: str = field(
        init=False,
        metadata={
            "sa": Column(
                String, default=lambda: idv2("purchase", version=1), primary_key=True
            )
        },
    )

    user_id: str = field(
        metadata={"sa": Column(String, ForeignKey("user.user_id"), primary_key=True)}
    )

    symbol: str = field(metadata={"sa": Column(String)})

    date: Optional[datetime] = field(
        metadata={"sa": Column(DateTime(timezone=True), nullable=True)},
    )

    quantity: Optional[float] = field(
        default_factory=float, metadata={"sa": Column(Float, nullable=False)}
    )

    price: Optional[float] = field(
        default_factory=float, metadata={"sa": Column(Float, nullable=False)}
    )

    # TODO add state -> options ["SOLD", "ACTIVE"]

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id", "symbol"],
            ["currency_pair.user_id", "currency_pair.symbol"],
            name="purchase_user_id_fkey",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )

    def gain(self, connection) -> float:  # TODO Add typing for arg connection
        return self.quantity * (
            float(get_symbol_ticker(connection, self.symbol).price) - self.price
        )
