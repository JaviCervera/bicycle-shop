from catalog.domain import Name, ProductId
from catalog.infrastructure import SqlAlchemyProductPartRepository


def init_product_part_repository(repo: SqlAlchemyProductPartRepository) -> None:
    parts = [
        (ProductId(1), Name('Frame type')),
        (ProductId(1), Name('Frame finish')),
        (ProductId(1), Name('Wheels')),
        (ProductId(1), Name('Rim color')),
        (ProductId(1), Name('Chain')),
    ]
    for part in parts:
        repo.create(*part)
    repo.commit()
