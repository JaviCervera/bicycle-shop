from dataclasses import dataclass

from .name import Name
from .model_id import ModelId

class ProductId(ModelId):
    pass

@dataclass(frozen=True)
class Product:
    id: ProductId
    name: Name
