from report_calculation.model import Base, mapper_registry
from dataclasses import dataclass, field
from typing import Optional
from sqlalchemy import Column, String, Float


@mapper_registry.mapped
@dataclass
class CryptoCurrency(Base):

    __tablename__ = "crypto_currency"

    __sa_dataclass_metadata_key__="sa"

    symbol: str = field(metadata={"sa": Column(String, primary_key=True)})
    price: float = field(metadata={"sa": Column(Float)})
    quantity: Optional[str] = field(metadata={"sa": Column(str, nullable=True)})

