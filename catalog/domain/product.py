from dataclasses import dataclass

from .description import Description
from .validations import validate_id

ProductId = int

@dataclass(frozen=True)
class Product:
    id: ProductId
    description: Description

    def __post_init__(self):
        validate_id(self.id, 'Product.id')
