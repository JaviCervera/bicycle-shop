from typing import Iterable

from sqlalchemy import create_engine

from catalog.domain import PartOption, PartOptionFilter, \
  PartOptionRepository, PriceCalculator, Product, ProductPart, \
  ProductPartRepository, ProductRepository
from catalog.sqlalchemy_infra import create_models, \
  SqlAlchemyPartOptionRepository, SqlAlchemyProductPartRepository, \
  SqlAlchemyProductRepository
from test.integration.init_part_option_repository import init_part_option_repository
from test.integration.init_product_part_repository import init_product_part_repository
from test.integration.init_product_reposity import init_product_repository


def main() -> None:
  engine = create_engine('sqlite+pysqlite:///:memory:')
  create_models(engine)
  product_repo = SqlAlchemyProductRepository(engine)
  part_repo = SqlAlchemyProductPartRepository(engine)
  option_repo = SqlAlchemyPartOptionRepository(engine)
  init_product_repository(product_repo)
  init_product_part_repository(part_repo)
  init_part_option_repository(option_repo)
  product = select_product(product_repo)
  options = select_parts(product, part_repo, option_repo)
  display_order_summary(product, options, part_repo, option_repo)


def select_product(repo: ProductRepository) -> Product:
  return select_elem(get_products(repo), 'product')


def select_parts(
    product: Product,
    part_repo: ProductPartRepository,
    option_repo: PartOptionRepository) -> Iterable[PartOption]:
  selected = []
  for part in get_parts(product, part_repo):
    selected.append(select_elem(
      filter_options(part, selected, option_repo), part.description.lower()))
  return selected


def select_elem(elems: Iterable, type: str):
  for i, elem in enumerate(elems):
    print(f'{i + 1}: {elem.description}')
  while True:
    selected = input(f'Select {type}: ')
    if not selected.isdigit() \
        or int(selected) not in range(1, len(elems) + 1):
      print(f'Please enter a number between 1 and {len(elems)}')
    else:
      print()
      return elems[int(selected) - 1]
    

def get_products(repo: ProductRepository) -> Iterable[Product]:
  return [repo.get(id) for id in repo.list()]


def get_parts(product: Product, repo: ProductPartRepository) -> Iterable[ProductPart]:
  return [repo.get(id) for id in repo.list(product.id)]


def filter_options(
    part: ProductPart,
    selection: Iterable[PartOption],
    repo: PartOptionRepository) -> Iterable[PartOption]:
  filter = PartOptionFilter(repo)
  return filter.in_stock(filter.compatible(part, selection))


def display_order_summary(
    product: Product,
    options: Iterable[PartOption],
    part_repo: ProductPartRepository,
    option_repo: PartOptionRepository) -> None:
  print()
  print(f'Your {product.description} order:')
  for opt in options:
    print(f'* {part_repo.get(opt.part_id).description}: {opt.description}')
  print()
  print(f'Total price: {PriceCalculator(option_repo)(options)}')


if __name__ == '__main__':
  main()
