from dataclasses import dataclass, field
from typing import Optional

from sqlalchemy import Column, Float, String

from report_calculation.model.base import Base, mapper_registry
from report_calculation.model.resource import Resource


@mapper_registry.mapped
@dataclass
class CurrencyPair(Base, Resource):

    __tablename__ = "currency_pair"

    __sa_dataclass_metadata_key__ = "sa"

    symbol: str = field(metadata={"sa": Column(String, primary_key=True)})
    quantity: Optional[float] = field(metadata={"sa": Column(Float, nullable=True)})

    def __str__(self) -> str:
        return f"Pair {self.symbol} with {self.quantity} tokens"
