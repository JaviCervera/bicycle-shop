from typing import Iterable

from catalog.domain import Product, ProductRepository
from .log import log

class ProductsAction:
    """ Use case to retrieve the products. """
    def __init__(self, repo: ProductRepository):
        self._repo = repo

    @log
    def __call__(self) -> Iterable[Product]:
        return [self._repo.get(id_)  # type: ignore
                    for id_ in self._repo.list()]
