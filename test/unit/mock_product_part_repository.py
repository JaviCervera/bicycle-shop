from typing import Iterable, Optional

from catalog.domain import ProductId, ProductPart, ProductPartId, \
    ProductPartRepository


class MockProductPartRepository(ProductPartRepository):
    def list(
            self,
            product_id: Optional[ProductId] = None) -> Iterable[ProductPartId]:
        if product_id in (None, 1):
            return [1, 2, 3, 4, 5]
        else:
            return []

    def get(self, id_: ProductPartId) -> Optional[ProductPart]:
        parts = [
            ProductPart(1, 1, 'Frame type'),
            ProductPart(2, 1, 'Frame finish'),
            ProductPart(3, 1, 'Wheels'),
            ProductPart(4, 1, 'Rim color'),
            ProductPart(5, 1, 'Chain'),
        ]
        if id_ in range(1, len(parts) + 1):
            return parts[id_ - 1]
        else:
            return None

    def create(self, product_id: ProductId, description: str) -> ProductPart:
        raise NotImplementedError()
