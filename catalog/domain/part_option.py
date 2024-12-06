from dataclasses import dataclass

from .description import Description
from .model_id import ModelId
from .product_part import ProductPartId
from .validations import validate_type

class PartOptionId(ModelId):
    pass


@dataclass(frozen=True)
class PartOption:
    id: PartOptionId
    part_id: ProductPartId
    description: Description
    price: float
    in_stock: bool

    def __post_init__(self):
        validate_type(self.price, (int, float), 'PartOption.price')
        validate_type(self.in_stock, bool, 'PartOption.in_stock')
