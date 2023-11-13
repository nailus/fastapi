from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.orm import as_declarative

NAMING_CONVENTION = {
    "column_names": lambda constraint, table: "_".join([column.name for column in constraint.columns.values()]),
    "ix": "ix__%(table_name)s__%(column_names)s",
    "uq": "uq__%(table_name)s__%(column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}


@as_declarative(metadata=MetaData(naming_convention=NAMING_CONVENTION))
class Base:
    id: Any
    __name__: str
