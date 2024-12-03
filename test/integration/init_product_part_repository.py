from catalog.sqlalchemy_infra import SqlAlchemyProductPartRepository


def init_product_part_repository(repo: SqlAlchemyProductPartRepository) -> None:
    parts = [
        (1, 'Frame type'),
        (1, 'Frame finish'),
        (1, 'Wheels'),
        (1, 'Rim color'),
        (1, 'Chain'),
    ]
    for part in parts:
        repo.create(*part)
    repo.commit()
