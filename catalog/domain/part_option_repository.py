from abc import ABC, abstractmethod
from typing import Iterable, Optional

from .models import PartOption

class PartOptionRepository(ABC):
  @abstractmethod
  def list(self, part_id: int = None) -> Iterable[int]:
    pass

  @abstractmethod
  def get(self, id: int) -> Optional[PartOption]:
    pass

  @abstractmethod
  def create(self, part_id: int, description: str, price: float, in_stock: bool) -> PartOption:
    pass

  @abstractmethod
  def list_incompatibilies(self, id: int) -> Iterable[int]:
    pass

  @abstractmethod
  def create_incompatibility(
      self, option_id: int, incompatible_option_id: int) -> None:
    pass

  @abstractmethod
  def list_depending_options(self, part_id: int) -> Iterable[int]:
    pass

  @abstractmethod
  def get_depending_option_price_coef(
      self, part_id: int, depending_option_id: int) -> float:
    pass
  
  @abstractmethod
  def create_depending_option(
      self, part_id: int, depending_option_id: int, coef: float) -> None:
    pass
