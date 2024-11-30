from typing import Optional, Sequence

from catalog.domain import ProductModel

class ProductModelRepository:
  def list(self, product_id: int = None) -> Sequence[int]:
    if product_id in (None, 1):
      return [1]
    else:
      return []

  def get(self, id: int) -> Optional[ProductModel]:
    if id == 1:
      return ProductModel(
        1,
        1,
        'BMX',
        'https://i5.walmartimages.com/asr/974013a6-f64c-4d26-aaa5-ac4077294a58_1.a6d127a1ba320fac589f825afa74a0b5.jpeg')
    else:
      return None
