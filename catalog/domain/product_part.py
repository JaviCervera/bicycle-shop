from dataclasses import dataclass

from .description import Description
from .product import ProductId
from .validations import validate_id

ProductPartId = int

@dataclass(frozen=True)
class ProductPart:
    id: ProductPartId
    product_id: ProductId
    description: Description

    def __post_init__(self):
        validate_id(self.id, 'ProductPart.id')
        validate_id(self.product_id, 'ProductPart.product_id')
