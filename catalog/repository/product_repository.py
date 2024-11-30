from typing import Optional, Sequence

from catalog.domain import Product


class ProductRepository:
  def list(self) -> Sequence[int]:
    return [1]

  def get(self, id: int) -> Optional[Product]:
    if id == 1:
      return Product(id, 'Bicycles')
    else:
      return None
