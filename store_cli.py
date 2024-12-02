from typing import Iterable

from sqlalchemy import create_engine

from catalog.application import CalculatePriceCommand, GetPartOptionsCommand, \
  GetProductPartsCommand, GetProductsCommand
from catalog.domain import PartOption, Product, ProductPart
from catalog.sqlalchemy_infra import create_models, \
  SqlAlchemyPartOptionRepository, SqlAlchemyProductPartRepository, \
  SqlAlchemyProductRepository
from test.integration.init_part_option_repository \
  import init_part_option_repository
from test.integration.init_product_part_repository \
  import init_product_part_repository
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
  get_products = GetProductsCommand(product_repo)
  get_parts = GetProductPartsCommand(part_repo)
  get_options = GetPartOptionsCommand(option_repo)
  calculate_price = CalculatePriceCommand(option_repo)
  product = select_product(get_products)
  options = select_parts(product, get_parts, get_options)
  display_order_summary(product, get_parts(product.id), options, calculate_price)


def select_product(get_products: GetProductsCommand) -> Product:
  return select_elem(get_products(), 'product')


def select_parts(
    product: Product,
    get_parts: GetProductPartsCommand,
    get_options: GetPartOptionsCommand) -> Iterable[PartOption]:
  selected = []
  for part in get_parts(product.id):
    selected.append(select_elem(
      get_options(part.id, selected), part.description.lower()))
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


def display_order_summary(
    product: Product,
    parts: Iterable[ProductPart],
    selected: Iterable[PartOption],
    calculate_price: CalculatePriceCommand) -> None:
  print()
  print(f'Your {product.description} order:')
  for opt in selected:
    part = [part for part in parts if part.id == opt.part_id][0]
    print(f'* {part.description}: {opt.description}')
  print()
  print(f'Total price: {calculate_price(selected)}')


if __name__ == '__main__':
  main()
