from catalog.sqlalchemy_infra import SqlAlchemyProductRepository


def init_product_repository(repo: SqlAlchemyProductRepository) -> None:
    repo.create('Bicycles')
    repo.commit()
