from dataclasses import dataclass

from .description import Description
from .model_id import ModelId
from .money import Money
from .product_part import ProductPartId

class PartOptionId(ModelId):
    pass


@dataclass(frozen=True)
class PartOption:
    id: PartOptionId
    part_id: ProductPartId
    description: Description
    price: Money
    in_stock: bool
