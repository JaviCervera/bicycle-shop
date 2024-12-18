from dataclasses import dataclass

from .name import Name
from .model_id import ModelId
from .product import ProductId

class ProductPartId(ModelId):
    pass

@dataclass(frozen=True)
class ProductPart:
    """
    Represents a type of part available for a product.
    For example: Wheels.
    """
    id: ProductPartId
    product_id: ProductId
    name: Name
