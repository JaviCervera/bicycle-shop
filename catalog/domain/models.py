from dataclasses import dataclass

@dataclass(frozen=True)
class Product:
  id: int
  description: str


@dataclass(frozen=True)
class ProductPart:
  id: int
  product_id: int
  description: str


@dataclass(frozen=True)
class PartOption:
  id: int
  part_id: int
  description: str
  price: float
  in_stock: bool
