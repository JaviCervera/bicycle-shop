from typing import Iterable, Optional
from catalog.domain import Name, Product, ProductId, ProductRepository


class MockProductRepository(ProductRepository):
    def list(self) -> Iterable[ProductId]:
        return [ProductId(1)]

    def get(self, id_: ProductId) -> Optional[Product]:
        if int(id_) == 1:
            return Product(ProductId(1), Name('Bicycles'))
        else:
            return None

    def create(self, name: Name) -> Product:
        raise NotImplementedError()
