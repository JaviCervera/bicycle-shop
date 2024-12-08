from abc import ABC, abstractmethod
from typing import Iterable, Optional

from .name import Name
from .product import ProductId
from .product_part import ProductPart, ProductPartId


class ProductPartRepository(ABC):
    @abstractmethod
    def list(
            self,
            product_id: Optional[ProductId] = None) -> Iterable[ProductPartId]:
        pass

    @abstractmethod
    def get(self, id_: ProductPartId) -> Optional[ProductPart]:
        pass

    @abstractmethod
    def create(
            self,
            product_id: ProductId,
            name: Name) -> ProductPart:
        pass
