from abc import ABC, abstractmethod
from typing import Iterable, Optional

from .models import ProductPart

class ProductPartRepository(ABC):
  @abstractmethod
  def list(self, product_id: int = None) -> Iterable[int]:
    pass

  @abstractmethod
  def get(self, id: int) -> Optional[ProductPart]:
    pass

  @abstractmethod
  def create(self, product_id: int, description: str) -> ProductPart:
    pass
