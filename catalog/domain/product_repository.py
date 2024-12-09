from abc import ABC, abstractmethod
from typing import Iterable, Optional

from .name import Name
from .product import Product, ProductId

class ProductRepository(ABC):
    """ A repository to get and put products in persistence. """
    @abstractmethod
    def list(self) -> Iterable[ProductId]:
        pass

    @abstractmethod
    def get(self, id_: ProductId) -> Optional[Product]:
        pass

    @abstractmethod
    def create(self, name: Name) -> Product:
        pass
