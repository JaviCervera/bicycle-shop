from dataclasses import dataclass

from .description import Description
from .model_id import ModelId
from .product import ProductId

class ProductPartId(ModelId):
    pass

@dataclass(frozen=True)
class ProductPart:
    id: ProductPartId
    product_id: ProductId
    description: Description
