from dataclasses import dataclass

from .validations import validate_id, validate_type

@dataclass(frozen=True)
class Product:
  id: int
  description: str

  def __post_init__(self):
    validate_id(self.id, 'Product.id')
    validate_type(self.description, str, 'Product.description')


@dataclass(frozen=True)
class ProductPart:
  id: int
  product_id: int
  description: str

  def __post_init__(self):
    validate_id(self.id, 'ProductPart.id')
    validate_id(self.product_id, 'ProductPart.product_id')
    validate_type(self.description, str, 'ProductPart.description')


@dataclass(frozen=True)
class PartOption:
  id: int
  part_id: int
  description: str
  price: float
  in_stock: bool

  def __post_init__(self):
    validate_id(self.id, 'PartOption.id')
    validate_id(self.part_id, 'PartOption.part_id')
    validate_type(self.description, str, 'PartOption.description')
    validate_type(self.price, (int, float), 'PartOption.price')
    validate_type(self.in_stock, bool, 'PartOption.in_stock')
