from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column

from catalog.domain import ProductId, ProductPart, ProductPartId, \
    ProductPartRepository
from .sqlalchemy_base import SqlAlchemyBase
from .sqlalchemy_base_repository import SqlAlchemyBaseRepository


class ProductPartModel(SqlAlchemyBase):
    __tablename__ = 'product_parts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int]
    description: Mapped[str]


class SqlAlchemyProductPartRepository(ProductPartRepository, SqlAlchemyBaseRepository):
    def list(
            self,
            product_id: Optional[ProductId] = None) -> Iterable[ProductPartId]:
        stmt = select(ProductPartModel.id)
        if product_id:
            stmt = stmt.where(ProductPartModel.product_id == product_id)
        return [row.id for row in self._session.execute(stmt).all()]

    def get(self, id_: ProductPartId) -> Optional[ProductPart]:
        result = self._session.scalars(
            select(ProductPartModel) \
                .where(ProductPartModel.id == id_)).first()
        return ProductPart(
            id=result.id,
            product_id=result.product_id,
            description=result.description) if result else None

    def create(self, product_id: ProductId, description: str) -> ProductPart:
        model = ProductPartModel(product_id=product_id, description=description)
        self._session.add(model)
        self._session.flush()
        return ProductPart(
            id=model.id,
            product_id=model.product_id,
            description=model.description)
