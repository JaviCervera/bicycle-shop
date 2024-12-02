from typing import Iterable

from catalog.domain import Product, ProductPart, ProductPartRepository
from catalog.domain.validations import validate_type

class GetProductPartsCommand:
  def __init__(self, repo: ProductPartRepository):
    validate_type(repo, ProductPartRepository, 'repo')
    self._repo = repo
  
  def __call__(self, product: Product) -> Iterable[ProductPart]:
    validate_type(product, Product, 'product')
    return [self._repo.get(id) for id in self._repo.list(product.id)]
