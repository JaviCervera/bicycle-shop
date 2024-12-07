from catalog.domain import Description, ProductId
from catalog.infrastructure import SqlAlchemyProductPartRepository


def init_product_part_repository(repo: SqlAlchemyProductPartRepository) -> None:
    parts = [
        (ProductId(1), Description('Frame type')),
        (ProductId(1), Description('Frame finish')),
        (ProductId(1), Description('Wheels')),
        (ProductId(1), Description('Rim color')),
        (ProductId(1), Description('Chain')),
    ]
    for part in parts:
        repo.create(*part)
    repo.commit()
