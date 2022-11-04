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
    def get_by_id(cls: Type[T], id: str) -> T:
        return db.session.query(cls).get(id)

    def update(self: T, **kwargs) -> T:
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)
        db.session.commit()
        return self

    def create(self: T) -> T:
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self: T) -> T:
        db.session.delete(self)
        return self
