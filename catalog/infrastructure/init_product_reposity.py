from catalog.domain import Description
from catalog.infrastructure import SqlAlchemyProductRepository


def init_product_repository(repo: SqlAlchemyProductRepository) -> None:
    repo.create(Description('Bicycles'))
    repo.commit()
