from dataclasses import asdict, dataclass, field
from typing import Any, Optional

from sqlalchemy import Column, Float, String

from report_calculation.model.base import Base, mapper_registry


@mapper_registry.mapped
@dataclass
class Currency(Base):

    __tablename__ = "crypto_currency"

    __sa_dataclass_metadata_key__ = "sa"

    symbol: str = field(metadata={"sa": Column(String, primary_key=True)})
    quantity: Optional[float] = field(metadata={"sa": Column(Float, nullable=True)})

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
