from typing import Type, TypeVar

from sqlalchemy.orm import registry

from report_calculation import db
from report_calculation.errors import NoDataFound

T = TypeVar("T", bound="Base")
mapper_registry = registry()


class Base:
    @classmethod
    def find(cls: Type[T], **filters) -> list[T]:
        query = db.session.query(cls)

        for_equality = True
        for key, value in filters.items():
            if key.startswith("!"):
                key = key[1:]
                for_equality = False

            column = getattr(cls, key)

            if for_equality:
                query = query.filter(column == value)
            else:
                query = query.filter(column != value)

        return query.all()

    @classmethod
    def get(cls: Type[T], **kwargs) -> T:
        query = db.session.query(cls)
        if not (result := query.get(kwargs)):
            raise NoDataFound(key=kwargs, messages="Not data found in DB")
        return result

    def update(self: T, force_update: bool = False, **kwargs) -> T:
        for key, value in kwargs.items():
            if force_update or value is not None:
                setattr(self, key, value)
        db.session.commit()
        return self

    def create(self: T) -> T:
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self: T) -> T:
        db.session.delete(self)
        db.session.commit()
        return self
