from typing import Type, TypeVar
from sqlalchemy.orm import registry
from report_calculation import db

T = TypeVar("T", bound="Base")
mapper_registry = registry()

class Base:
    @classmethod
    def get_all(cls: Type[T]) -> list[T]:
        return db.session.query(cls).all()
    
    @classmethod
    def get_by_id(cls: Type[T]) -> list[T]:
        return db.session.query(cls).get(id)
