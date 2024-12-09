from dataclasses import dataclass

from .name import Name
from .model_id import ModelId
from .money import Money
from .product_part import ProductPartId
from .units import Units

class PartOptionId(ModelId):
    pass


@dataclass(frozen=True)
class PartOption:
    """ An option for a part. For example: Mountain wheels. """
    id: PartOptionId
    part_id: ProductPartId
    name: Name
    price: Money
    available_units: Units

    @property
    def in_stock(self) -> bool:
        return int(self.available_units) > 0
