from abc import ABC
from typing import Self

from sqlalchemy import Engine
from sqlalchemy.orm import Session

class SqlAlchemyBaseRepository(ABC):
    """
    Base class of all SQLAlchemy based repositories.
    Provides context management.
    """
    def __init__(self, engine: Engine):
        self._engine = engine
        self._session = Session(engine)

    def commit(self) -> None:
        if self._session:
            self._session.commit()

    def close(self) -> None:
        if self._session:
            self._session.close()
        self._session = None  # type: ignore

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args) -> None:
        self.commit()
        self.close()
