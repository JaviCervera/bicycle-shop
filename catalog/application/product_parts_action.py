from logging import Logger
from typing import Iterable

from catalog.domain import ProductId, ProductPart, ProductPartRepository
from catalog.domain.validations import validate_type


class ProductPartsAction:
    def __init__(self, repo: ProductPartRepository, logger: Logger):
        validate_type(repo, ProductPartRepository, 'repo')
        validate_type(logger, Logger, 'logger')
        self._repo = repo
        self._logger = logger

    def __call__(self, product_id: ProductId) -> Iterable[ProductPart]:
        self._logger.info(f'ProductPartsAction({product_id}) called')
        validate_type(product_id, ProductId, 'product_id')
        parts = [self._repo.get(id_)
                 for id_ in self._repo.list(product_id)]
        self._logger.info(f'ProductPartsAction({product_id}) result: {parts}')
        return parts  # type: ignore
