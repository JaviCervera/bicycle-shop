from typing import Iterable

from catalog.domain import Product, ProductRepository
from catalog.domain.validations import validate_type


class ProductsAction:
    def __init__(self, repo: ProductRepository):
        validate_type(repo, ProductRepository, 'repo')
        self._repo = repo

    def __call__(self) -> Iterable[Product]:
        return [self._repo.get(id_) for id_ in self._repo.list()]  # type: ignore
