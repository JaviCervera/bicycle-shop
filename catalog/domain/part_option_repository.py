from abc import ABC, abstractmethod
from typing import Iterable, Optional

from .money import Money
from .name import Name
from .part_option import PartOption, PartOptionId
from .product_part import ProductPartId
from .units import Units

class PartOptionRepository(ABC):
    """ A repository to get and put part options in persistence. """
    @abstractmethod
    def list(
            self,
            part_id: Optional[ProductPartId] = None) -> Iterable[PartOptionId]:
        pass

    @abstractmethod
    def get(self, id_: PartOptionId) -> Optional[PartOption]:
        pass

    @abstractmethod
    def create(
            self,
            part_id: ProductPartId,
            name: Name,
            price: Money,
            available_units: Units) -> PartOption:
        pass

    @abstractmethod
    def list_incompatibilities(
            self, id_: PartOptionId) -> Iterable[PartOptionId]:
        pass

    @abstractmethod
    def create_incompatibility(
            self,
            option_id: PartOptionId,
            incompatible_option_id: PartOptionId) -> None:
        pass

    @abstractmethod
    def list_depending_options(
            self, part_id: ProductPartId) -> Iterable[PartOptionId]:
        pass

    @abstractmethod
    def get_depending_option_price_coef(
            self,
            part_id: ProductPartId,
            depending_option_id: PartOptionId) -> float:
        pass

    @abstractmethod
    def create_depending_option(
            self,
            part_id: ProductPartId,
            depending_option_id:
            PartOptionId,
            coefficient: float) -> None:
        pass
