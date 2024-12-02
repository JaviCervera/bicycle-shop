from dataclasses import dataclass

@dataclass(frozen=True)
class Product:
  id: int
  description: str

  def __post_init__(self):
    validate_id(self.id, 'Product.id')
    validate_str(self.description, 'Product.description')


@dataclass(frozen=True)
class ProductPart:
  id: int
  product_id: int
  description: str

  def __post_init__(self):
    validate_id(self.id, 'ProductPart.id')
    validate_int(self.product_id, 'ProductPart.product_id')
    validate_str(self.description, 'ProductPart.description')


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
    validate_str(self.description, 'PartOption.description')
    validate_float(self.price, 'PartOption.price')
    validate_bool(self.in_stock, 'PartOption.in_stock')


def validate_id(id, field: str) -> None:
  if not isinstance(id, int) or not id > 0:
    raise ValueError(f'{field} must be a positive integer, '
                     f'got {type(id).__name__}')


def validate_bool(v, field: str) -> None:
  if not isinstance(v, bool):
    raise ValueError(f'{field} must be a boolean, got {type(v).__name__}')


def validate_int(v, field: str) -> None:
  if not isinstance(v, int):
    raise ValueError(f'{field} must be an integer, got {type(v).__name__}')
  

def validate_float(v, field: str) -> None:
  if not isinstance(v, (int, float)):
    raise ValueError(f'{field} must be a float, got {type(v).__name__}')


def validate_str(v, field: str) -> None:
  if not isinstance(v, str) or not v:
    raise ValueError(f'{field} must be a non empty string, '
                     f'got {type(v).__name__}')
