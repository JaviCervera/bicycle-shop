from catalog.domain import Name
from catalog.infrastructure import SqlAlchemyProductRepository


def init_product_repository(repo: SqlAlchemyProductRepository) -> None:
    repo.create(Name('Bicycles'))
    repo.commit()
