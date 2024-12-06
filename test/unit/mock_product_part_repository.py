from typing import Iterable, Optional

from catalog.domain import Description, ProductId, ProductPart, \
    ProductPartId, ProductPartRepository


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
            ProductPart(1, 1, Description('Frame type')),
            ProductPart(2, 1, Description('Frame finish')),
            ProductPart(3, 1, Description('Wheels')),
            ProductPart(4, 1, Description('Rim color')),
            ProductPart(5, 1, Description('Chain')),
        ]
        if id_ in range(1, len(parts) + 1):
            return parts[id_ - 1]
        else:
            return None

    def create(
            self,
            product_id: ProductId,
            description: Description) -> ProductPart:
        raise NotImplementedError()
