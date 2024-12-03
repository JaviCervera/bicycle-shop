from typing import Iterable

from catalog.application import GetPartOptionsCommand, GetProductPartsCommand, \
  GetProductsCommand
from catalog.domain import PartOption, Product, ProductPart

from catalog_application import create_catalog_app

catalog = create_catalog_app('http://localhost:8080')


def main() -> None:
  product = select_product(catalog.get_products)
  options = select_parts(
    product, catalog.get_product_parts, catalog.get_part_options)
  display_order_summary(
    product,
    catalog.get_product_parts(product.id),
    options,
    catalog.calculate_price(options))


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
    price: float) -> None:
  print()
  print(f'Your {product.description} order:')
  for opt in selected:
    part = [part for part in parts if part.id == opt.part_id][0]
    print(f'* {part.description}: {opt.description}')
  print()
  print(f'Total price: {price}')


if __name__ == '__main__':
  main()
