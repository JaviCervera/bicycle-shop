from catalog.domain import Description
from catalog.sqlalchemy_infra import SqlAlchemyProductPartRepository


def init_product_part_repository(repo: SqlAlchemyProductPartRepository) -> None:
    parts = [
        (1, Description('Frame type')),
        (1, Description('Frame finish')),
        (1, Description('Wheels')),
        (1, Description('Rim color')),
        (1, Description('Chain')),
    ]
    for part in parts:
        repo.create(*part)
    repo.commit()
