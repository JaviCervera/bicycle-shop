from typing import Iterable, Optional

from catalog.domain import Product


class ProductRepository:
  def list(self) -> Iterable[int]:
    return [1]

  def get(self, id: int) -> Optional[Product]:
    if id == 1:
      return Product(id, 'Bicycles')
    else:
      return None
