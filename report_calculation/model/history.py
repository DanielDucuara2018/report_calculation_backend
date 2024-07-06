from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import Column, Float, String
from sqlalchemy.sql.schema import ForeignKey

from report_calculation.model.base import Base, mapper_registry
from report_calculation.model.resource import Resource
from report_calculation.utils import idv2


@mapper_registry.mapped
@dataclass
class Portafolio(Base, Resource):

    __tablename__ = "portafolio"

    __sa_dataclass_metadata_key__ = "sa"

    portafolio_id: str = field(
        init=False,
        metadata={
            "sa": Column(
                String,
                default=lambda: idv2("portafolio_id", version=1),
                primary_key=True,
            )
        },
    )

    user_id: str = field(metadata={"sa": Column(String, ForeignKey("user.user_id"))})

    total_euros: float = field(metadata={"sa": Column(Float, nullable=False)})

    total_currency: float = field(metadata={"sa": Column(Float, nullable=False)})

    profit_currency: float = field(metadata={"sa": Column(Float, nullable=False)})

    investment: float = field(metadata={"sa": Column(Float, nullable=False)})
