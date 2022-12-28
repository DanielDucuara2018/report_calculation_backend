from typing import Optional, Type, TypeVar, Union

from sqlalchemy.orm import registry

from report_calculation import db
from report_calculation.errors import NotDataFound

T = TypeVar("T", bound="Base")
mapper_registry = registry()


class Base:
    @classmethod
    def get(cls: Type[T], id: Optional[str] = None) -> Union[T, list[T]]:
        query = db.session.query(cls)
        if id:
            result = query.get(id)
            if not result:
                raise NotDataFound(id=id, messages="Not data found in DB")
        else:
            result = query.all()
        return result

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
        db.session.commit()
        return self
