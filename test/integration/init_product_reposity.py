from catalog.domain import ProductRepository

def init_product_repository(repo: ProductRepository) -> None:
  repo.create('Bicycles')
  repo.commit()
