from sqlalchemy import Engine
from sqlalchemy.orm import DeclarativeBase


class SqlAlchemyBase(DeclarativeBase):
    """ Base class used internally to define all SQLAlchemy tables """
    pass


def create_models(engine: Engine) -> None:
    SqlAlchemyBase.metadata.create_all(engine)
