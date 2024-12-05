from typing import Iterable

from catalog.domain import ProductId, ProductPart, ProductPartRepository
from catalog.domain.validations import validate_type


class GetProductPartsCommand:
    def __init__(self, repo: ProductPartRepository):
        validate_type(repo, ProductPartRepository, 'repo')
        self._repo = repo

    def __call__(self, product_id: ProductId) -> Iterable[ProductPart]:
        validate_type(product_id, ProductId, 'product_id')
        return [self._repo.get(id_) for id_ in self._repo.list(product_id)]  # type: ignore
