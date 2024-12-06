from dataclasses import dataclass

from .description import Description
from .model_id import ModelId

class ProductId(ModelId):
    pass

@dataclass(frozen=True)
class Product:
    id: ProductId
    description: Description
