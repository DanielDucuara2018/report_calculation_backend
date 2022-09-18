from typing import Optional, Type, TypeVar

from sqlalchemy.orm import registry

from  report_calculation import db

T = TypeVar("T", bound="Base")
mapper_registry = registry()


class Base:
    @classmethod
    def get(cls: Type[T], id: str) -> Optional[T]:
        return db.session.query(cls).get(id)