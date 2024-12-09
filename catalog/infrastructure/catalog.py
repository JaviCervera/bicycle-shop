from typing import Self

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from catalog.application import PartOptionsAction, PartOptionsPriceAction, \
    ProductPartsAction, ProductsAction
from .sqlalchemy_base import create_models
from .sqlalchemy_part_option_repository import SqlAlchemyPartOptionRepository
from .sqlalchemy_product_part_repository import SqlAlchemyProductPartRepository
from .sqlalchemy_product_repository import SqlAlchemyProductRepository


class Catalog:
    """
    A class that encapsulates the application layer, providing access to the
    use cases and an implementation of the repositories based on SQLAlchemy,
    which support "with" context to ensure that repositories commit as they
    exit the context.
    """
    def __init__(self, db_url: str, echo=False):
        engine = create_engine(db_url, echo=echo)
        create_models(engine)
        self.session = Session(engine)
        self.product_repo = SqlAlchemyProductRepository(self.session)
        self.part_repo = SqlAlchemyProductPartRepository(self.session)
        self.option_repo = SqlAlchemyPartOptionRepository(self.session)
        self.products = ProductsAction(self.product_repo)
        self.product_parts = ProductPartsAction(self.part_repo)
        self.part_options = PartOptionsAction(self.option_repo)
        self.part_options_price = PartOptionsPriceAction(self.option_repo)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args) -> None:
        self.session.commit()
        self.session.close()
