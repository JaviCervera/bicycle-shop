from typing import Iterable, Optional

from catalog.domain import ProductPart, ProductPartRepository

class MockProductPartRepository(ProductPartRepository):
  def list(self, product_id: int = None) -> Iterable[int]:
    if product_id in (None, 1):
      return [1, 2, 3, 4, 5]
    else:
      return []

  def get(self, id: int) -> Optional[ProductPart]:
    parts = [
      ProductPart(1, 1, 'Frame type'),
      ProductPart(2, 1, 'Frame finish'),
      ProductPart(3, 1, 'Wheels'),
      ProductPart(4, 1, 'Rim color'),
      ProductPart(5, 1, 'Chain'),
    ]
    if id in range(1, len(parts) + 1):
      return parts[id - 1]
    else:
      return None

  def create(self, product_id: int, description: str) -> ProductPart:
    pass
