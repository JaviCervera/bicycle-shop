from typing import Iterable, Optional

from sqlalchemy import Engine, select
from sqlalchemy.orm import Mapped, mapped_column, Session

from catalog.domain import ProductPart, ProductPartRepository
from .sqlalchemy_base import SqlAlchemyBase

class ProductPartModel(SqlAlchemyBase):
  __tablename__ = 'product_parts'
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  product_id: Mapped[int]
  description: Mapped[str]


class SqlAlchemyProductPartRepository(ProductPartRepository):
  def __init__(self, engine: Engine):
    self._engine = engine
    self._session = Session(engine)

  def list(self, product_id: int = None) -> Iterable[int]:
    stmt = select(ProductPartModel.id)
    if product_id:
      stmt = stmt.where(ProductPartModel.product_id == product_id)
    return [row.id for row in self._session.execute(stmt).all()]

  def get(self, id: int) -> Optional[ProductPart]:
    result = self._session.scalars(
      select(ProductPartModel) \
        .where(ProductPartModel.id == id)).first()
    return ProductPart(
      id=result.id,
      product_id=result.product_id,
      description=result.description) if result else None
  
  def create(self, product_id: int, description: str) -> ProductPart:
    model = ProductPartModel(product_id=product_id, description=description)
    self._session.add(model)
    self._session.flush()
    return ProductPartModel(
      id=model.id,
      product_id=model.product_id,
      description=model.description)

  def commit(self) -> None:
    self._session.commit()
  
  def close(self) -> None:
    self._session.close()

  def __enter__(self) -> 'SqlAlchemyProductPartRepository':
    return self
  
  def __exit__(self, *args) -> None:
    self.close()
