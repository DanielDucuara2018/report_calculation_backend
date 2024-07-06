from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, Float, LargeBinary, String
from sqlalchemy.orm import relationship

from report_calculation.model.base import Base, mapper_registry
from report_calculation.model.exchange import Exchange

# from report_calculation.model.history import Portafolio as PortafolioHistory
from report_calculation.model.purchase import Purchase
from report_calculation.model.resource import Resource
from report_calculation.model.telegram import Telegram
from report_calculation.utils import generate_password_hash, idv2

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

    username: str = field(metadata={"sa": Column("user_name", String, nullable=False)})

    _password: bytes = field(
        metadata={"sa": Column("password", LargeBinary, nullable=False)}
    )

    email: Optional[str] = field(metadata={"sa": Column(String)})

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
        metadata={"sa": relationship("CurrencyPair", uselist=True)},
    )

    # association between User -> Purchases
    purchases: list["Purchase"] = field(
        default_factory=list,
        metadata={"sa": relationship("Purchase", uselist=True, overlaps="purchases")},
    )

    # association between User -> Telegram
    telegrams: list["Telegram"] = field(
        default_factory=list,
        metadata={"sa": relationship("Telegram", uselist=True)},
    )

    # association between User -> Exchange
    exchanges: list["Exchange"] = field(
        default_factory=list,
        metadata={"sa": relationship("Exchange", uselist=True)},
    )

    # association between User -> Exchange
    # portafolio: list["PortafolioHistory"] = field(
    #     default_factory=list,
    #     metadata={"sa": relationship("Portafolio", uselist=True)},
    # )

    @property
    def active_telgram_bot(self) -> Optional[Telegram]:
        if self.telegrams:
            return self.telegrams[0]
        return None

    @property
    def active_exchange(self) -> Optional[Exchange]:
        if self.exchanges:
            return self.exchanges[0]
        return None

    @property
    def password(self) -> bytes:
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = generate_password_hash(value)
