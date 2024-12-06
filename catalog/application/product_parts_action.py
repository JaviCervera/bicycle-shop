from typing import Iterable

from catalog.domain import ProductId, ProductPart, ProductPartRepository
from .log import log

class ProductPartsAction:
    def __init__(self, repo: ProductPartRepository):
        self._repo = repo

    @log
    def __call__(self, product_id: ProductId) -> Iterable[ProductPart]:
        return [self._repo.get(id_)  # type: ignore
                for id_ in self._repo.list(product_id)]
