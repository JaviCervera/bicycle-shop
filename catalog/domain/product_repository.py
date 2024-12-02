from abc import ABC, abstractmethod
from typing import Iterable, Optional

from .models import Product

class ProductRepository(ABC):
  @abstractmethod
  def list(self) -> Iterable[int]:
    pass

  @abstractmethod
  def get(self, id: int) -> Optional[Product]:
    pass
