from logging import Logger
from typing import Iterable

from catalog.domain import Product, ProductRepository
from catalog.domain.validations import validate_type


class ProductsAction:
    def __init__(self, repo: ProductRepository, logger: Logger):
        validate_type(repo, ProductRepository, 'repo')
        validate_type(logger, Logger, 'logger')
        self._repo = repo
        self._logger = logger

    def __call__(self) -> Iterable[Product]:
        self._logger.info('ProductsAction called')
        products = [self._repo.get(id_)
                    for id_ in self._repo.list()]
        self._logger.info(f'ProductsAction result: {products}')
        return products  # type: ignore
