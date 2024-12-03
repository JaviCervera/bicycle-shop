from dataclasses import dataclass

from .validations import validate_id, validate_type

ProductId = int

@dataclass(frozen=True)
class Product:
    id: ProductId
    description: str

    def __post_init__(self):
        validate_id(self.id, 'Product.id')
        validate_type(self.description, str, 'Product.description')
