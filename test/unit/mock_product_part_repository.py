from typing import Iterable, Optional

from catalog.domain import Name, ProductId, ProductPart, \
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
                ProductPartId(1), ProductId(1), Name('Frame type')),
            ProductPart(
                ProductPartId(2), ProductId(1), Name('Frame finish')),
            ProductPart(
                ProductPartId(3), ProductId(1), Name('Wheels')),
            ProductPart(
                ProductPartId(4), ProductId(1), Name('Rim color')),
            ProductPart(
                ProductPartId(5), ProductId(1), Name('Chain')),
        ]
        if int(id_) in range(1, len(parts) + 1):
            return parts[int(id_) - 1]
        else:
            return None

    def create(
            self,
            product_id: ProductId,
            name: Name) -> ProductPart:
        raise NotImplementedError()
