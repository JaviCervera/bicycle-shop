from typing import Self

from sqlalchemy import create_engine

from catalog.application import PartOptionsAction, PartOptionsPriceAction, \
    ProductPartsAction, ProductsAction
from .sqlalchemy_base import create_models
from .sqlalchemy_part_option_repository import SqlAlchemyPartOptionRepository
from .sqlalchemy_product_part_repository import SqlAlchemyProductPartRepository
from .sqlalchemy_product_repository import SqlAlchemyProductRepository


class Catalog:
    def __init__(self, url: str, echo=False):
        engine = create_engine(url, echo=echo)
        create_models(engine)
        self.product_repo = SqlAlchemyProductRepository(engine)
        self.part_repo = SqlAlchemyProductPartRepository(engine)
        self.option_repo = SqlAlchemyPartOptionRepository(engine)
        self.products = ProductsAction(self.product_repo)
        self.product_parts = ProductPartsAction(self.part_repo)
        self.part_options = PartOptionsAction(self.option_repo)
        self.part_options_price = PartOptionsPriceAction(self.option_repo)

    def __enter__(self) -> Self:
        self.product_repo.__enter__()
        self.part_repo.__enter__()
        self.option_repo.__enter__()
        return self

    def __exit__(self, *args) -> None:
        self.product_repo.__exit__()
        self.part_repo.__exit__()
        self.option_repo.__exit__()
