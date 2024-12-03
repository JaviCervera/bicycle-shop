from abc import ABC, abstractmethod
from typing import Iterable, Optional

from .product import ProductId
from .product_part import ProductPart, ProductPartId


class ProductPartRepository(ABC):
    @abstractmethod
    def list(self, product_id: ProductId = None) -> Iterable[ProductPartId]:
        pass

    @abstractmethod
    def get(self, id_: ProductPartId) -> Optional[ProductPart]:
        pass

    @abstractmethod
    def create(self, product_id: ProductId, description: str) -> ProductPart:
        pass
