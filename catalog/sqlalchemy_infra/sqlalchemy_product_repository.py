from typing import Iterable, Optional

from sqlalchemy import Engine, select
from sqlalchemy.orm import Mapped, mapped_column, Session

from catalog.domain import Product, ProductId, ProductRepository
from .sqlalchemy_base import SqlAlchemyBase


class ProductModel(SqlAlchemyBase):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str]


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, engine: Engine):
        self._engine = engine
        self._session = Session(engine)

    def list(self) -> Iterable[ProductId]:
        return [row.id
                for row in self._session.execute(select(ProductModel.id)).all()]

    def get(self, id_: ProductId) -> Optional[Product]:
        result = self._session.scalars(
            select(ProductModel) \
                .where(ProductModel.id == id_)).first()
        return Product(result.id, result.description) if result else None

    def create(self, description: str) -> Product:
        model = ProductModel(id=None, description=description)
        self._session.add(model)
        self._session.flush()
        return Product(model.id, model.description)

    def commit(self) -> None:
        self._session.commit()

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> 'SqlAlchemyProductRepository':
        return self

    def __exit__(self, *args) -> None:
        self.close()
