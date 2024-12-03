from dataclasses import dataclass

from .product_part import ProductPartId
from .validations import validate_id, validate_type

PartOptionId = int


@dataclass(frozen=True)
class PartOption:
    id: PartOptionId
    part_id: ProductPartId
    description: str
    price: float
    in_stock: bool

    def __post_init__(self):
        validate_id(self.id, 'PartOption.id')
        validate_id(self.part_id, 'PartOption.part_id')
        validate_type(self.description, str, 'PartOption.description')
        validate_type(self.price, (int, float), 'PartOption.price')
        validate_type(self.in_stock, bool, 'PartOption.in_stock')
