from dataclasses import dataclass

from .name import Name
from .model_id import ModelId
from .money import Money
from .product_part import ProductPartId

class PartOptionId(ModelId):
    pass


@dataclass(frozen=True)
class PartOption:
    id: PartOptionId
    part_id: ProductPartId
    name: Name
    price: Money
    in_stock: bool
