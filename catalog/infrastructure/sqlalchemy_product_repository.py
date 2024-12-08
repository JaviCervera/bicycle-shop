from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column

from catalog.domain import Name, Product, ProductId, ProductRepository
from .sqlalchemy_base import SqlAlchemyBase
from .sqlalchemy_base_repository import SqlAlchemyBaseRepository


class ProductModel(SqlAlchemyBase):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]


class SqlAlchemyProductRepository(ProductRepository, SqlAlchemyBaseRepository):
    def list(self) -> Iterable[ProductId]:
        return [ProductId(row.id)
                for row in self._session.execute(select(ProductModel.id)).all()]

    def get(self, id_: ProductId) -> Optional[Product]:
        result = self._session.scalars(
            select(ProductModel) \
                .where(ProductModel.id == int(id_))).first()
        return Product(ProductId(result.id), Name(result.name)) \
            if result else None

    def create(self, name: Name) -> Product:
        model = ProductModel(name=str(name))
        self._session.add(model)
        self._session.flush()
        return Product(ProductId(model.id), Name(model.name))
