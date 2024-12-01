from typing import Iterable

from catalog.application import PartOptionFilter, PartOptionRepository, \
  PriceCalculator, ProductPartRepository, ProductRepository
from catalog.domain import PartOption, Product, ProductPart


def main() -> None:
  product = select_product()
  options = select_parts(product)
  display_order_summary(product, options)


def select_product() -> Product:
  return select_elem(get_products(), 'product')


def select_parts(product: Product) -> Iterable[PartOption]:
  selected = []
  for part in get_parts(product):
    selected.append(
      select_elem(filter_options(part, selected), part.description.lower()))
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
    

def get_products() -> Iterable[Product]:
  repo = ProductRepository()
  return [repo.get(id) for id in repo.list()]


def get_parts(product: Product) -> Iterable[ProductPart]:
  repo = ProductPartRepository()
  return [repo.get(id) for id in repo.list(product.id)]


def filter_options(
    part: ProductPart,
    selection: Iterable[PartOption]) -> Iterable[PartOption]:
  filter = PartOptionFilter(PartOptionRepository())
  return filter.in_stock(filter.compatible(part, selection))


def display_order_summary(
    product: Product, options: Iterable[PartOption]) -> None:
  part_repo = ProductPartRepository()
  print()
  print(f'Your {product.description} order:')
  for opt in options:
    print(f'* {part_repo.get(opt.part_id).description}: {opt.description}')
  print()
  print(f'Total price: {PriceCalculator(PartOptionRepository())(options)}')


if __name__ == '__main__':
  main()
