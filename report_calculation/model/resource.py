from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func


@dataclass
class Resource:

    __sa_dataclass_metadata_key__ = "sa"

    description: Optional[str] = field(metadata={"sa": Column(String)})

    update_date: Optional[datetime] = field(
        init=False,
        metadata={
            "sa": Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
        },
    )

    creation_date: datetime = field(
        init=False, metadata={"sa": Column(DateTime(timezone=True), default=func.now())}
    )
