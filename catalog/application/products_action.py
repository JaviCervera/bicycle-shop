from logging import Logger
from typing import Iterable

from catalog.domain import Product, ProductRepository


class ProductsAction:
    def __init__(self, repo: ProductRepository, logger: Logger):
        self._repo = repo
        self._logger = logger

    def __call__(self) -> Iterable[Product]:
        self._logger.info('ProductsAction called')
        products = [self._repo.get(id_)
                    for id_ in self._repo.list()]
        self._logger.info(f'ProductsAction result: {products}')
        return products  # type: ignore
