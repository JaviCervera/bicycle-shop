from dataclasses import dataclass

from .name import Name
from .model_id import ModelId

class ProductId(ModelId):
    pass

@dataclass(frozen=True)
class Product:
    """ A product. For example: Bicycles. """
    id: ProductId
    name: Name
