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

    user_id: str = field(metadata={"sa": Column(String, ForeignKey("user.user_id"))})

    symbol: str = field(metadata={"sa": Column(String)})

    quantity: Optional[float] = field(
        metadata={"sa": Column(Float, default=float(0), nullable=False)}
    )

    price: Optional[float] = field(
        metadata={"sa": Column(Float, default=float(0), nullable=False)}
    )

    date: Optional[datetime] = field(
        metadata={"sa": Column(DateTime(timezone=True), nullable=True)},
    )

    # TODO add state -> options ["SOLD", "ACTIVE"]

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id", "symbol"],
            ["currency_pair.user_id", "currency_pair.symbol"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )

    @property
    def gain(self) -> float:
        return self.quantity * (
            float(get_symbol_ticker(self.symbol).price) - self.price
        )
