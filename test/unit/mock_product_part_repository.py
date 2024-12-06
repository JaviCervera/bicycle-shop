from typing import Iterable, Optional

from catalog.domain import Description, ProductId, ProductPart, \
    ProductPartId, ProductPartRepository


class MockProductPartRepository(ProductPartRepository):
    def list(
            self,
            product_id: Optional[ProductId] = None) -> Iterable[ProductPartId]:
        if product_id in (None, 1):
            return [
                ProductPartId(1),
                ProductPartId(2),
                ProductPartId(3),
                ProductPartId(4),
                ProductPartId(5)]
        else:
            return []

    def get(self, id_: ProductPartId) -> Optional[ProductPart]:
        parts = [
            ProductPart(
                ProductPartId(1), ProductId(1), Description('Frame type')),
            ProductPart(
                ProductPartId(2), ProductId(1), Description('Frame finish')),
            ProductPart(
                ProductPartId(3), ProductId(1), Description('Wheels')),
            ProductPart(
                ProductPartId(4), ProductId(1), Description('Rim color')),
            ProductPart(
                ProductPartId(5), ProductId(1), Description('Chain')),
        ]
        if int(id_) in range(1, len(parts) + 1):
            return parts[int(id_) - 1]
        else:
            return None

    def create(
            self,
            product_id: ProductId,
            description: Description) -> ProductPart:
        raise NotImplementedError()
