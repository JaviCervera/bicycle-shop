from catalog.domain import Name
from catalog.infrastructure import SqlAlchemyProductRepository


def init_product_repository(repo: SqlAlchemyProductRepository) -> None:
    """
    Utility function that initialized a SqlAlchemyProductRepository with
    test data.
    """
    repo.create(Name('Bicycles'))
