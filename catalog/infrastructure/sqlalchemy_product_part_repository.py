from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column, Session

from catalog.domain import Name, ProductId, ProductPart, \
    ProductPartId, ProductPartRepository
from .sqlalchemy_base import SqlAlchemyBase


class ProductPartModel(SqlAlchemyBase):
    __tablename__ = 'product_parts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int]
    name: Mapped[str]


class SqlAlchemyProductPartRepository(ProductPartRepository):
    """ A SQLAlchemy-based implementation of ProductPartRepository. """
    def __init__(self, session: Session):
        self._session = session

    def list(
            self,
            product_id: Optional[ProductId] = None) -> Iterable[ProductPartId]:
        stmt = select(ProductPartModel.id)
        if product_id:
            stmt = stmt.where(ProductPartModel.product_id == int(product_id))
        return [row.id for row in self._session.execute(stmt).all()]

    def get(self, id_: ProductPartId) -> Optional[ProductPart]:
        result = self._session.scalars(
            select(ProductPartModel) \
                .where(ProductPartModel.id == int(id_))).first()
        return ProductPart(
            id=ProductPartId(result.id),
            product_id=ProductId(result.product_id),
            name=Name(result.name)) if result else None

    def create(
            self,
            product_id: ProductId,
            name: Name) -> ProductPart:
        model = ProductPartModel(
            product_id=int(product_id),
            name=str(name))
        self._session.add(model)
        self._session.flush()
        return ProductPart(
            id=ProductPartId(model.id),
            product_id=ProductId(model.product_id),
            name=Name(model.name))
