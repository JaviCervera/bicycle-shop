from dataclasses import dataclass

from .description import Description
from .model_id import ModelId
from .product_part import ProductPartId

class PartOptionId(ModelId):
    pass


@dataclass(frozen=True)
class PartOption:
    id: PartOptionId
    part_id: ProductPartId
    description: Description
    price: float
    in_stock: bool
