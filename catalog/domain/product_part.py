from dataclasses import dataclass

from .product import ProductId
from .validations import validate_id, validate_type

ProductPartId = int

@dataclass(frozen=True)
class ProductPart:
    id: ProductPartId
    product_id: ProductId
    description: str

    def __post_init__(self):
        validate_id(self.id, 'ProductPart.id')
        validate_id(self.product_id, 'ProductPart.product_id')
        validate_type(self.description, str, 'ProductPart.description')
