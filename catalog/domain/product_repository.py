from abc import ABC, abstractmethod
from typing import Iterable, Optional

from .description import Description
from .product import Product, ProductId

class ProductRepository(ABC):
    @abstractmethod
    def list(self) -> Iterable[ProductId]:
        pass

    @abstractmethod
    def get(self, id_: ProductId) -> Optional[Product]:
        pass

    @abstractmethod
    def create(self, description: Description) -> Product:
        pass
