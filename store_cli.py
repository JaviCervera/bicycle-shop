import os
from typing import Callable, Iterable, Union

import requests

from catalog.domain import PartOption, Product, ProductId, ProductPart, \
    ProductPartId
from catalog.sqlalchemy_infra import Application

GetPartOptionsFunc = \
    Callable[[ProductPartId, Iterable[PartOption]], Iterable[PartOption]]

class ApplicationProxy:
    def __init__(self, url: str) -> None:
        self._base_url = url

    def calculate_price(self, selected: Iterable[PartOption]) -> float:
        result = requests.get(os.path.join(self._base_url, 'price'), params={
            'selected_options': self._join_options(selected),
        })
        result.raise_for_status()
        return float(result.json()['price'])

    @staticmethod
    def _join_options(options: Iterable[PartOption]) -> str:
        return ','.join([str(opt.id) for opt in options])

    def get_part_options(
            self,
            part_id: ProductPartId,
            selected: Iterable[PartOption]) -> Iterable[PartOption]:
        result = requests.get(os.path.join(self._base_url, 'part_options'), params={
            'product_part': part_id,
            'selected_options': self._join_options(selected),
        })
        result.raise_for_status()
        return [PartOption(**opt) for opt in result.json()]

    def get_product_parts(self, product_id: ProductId) -> Iterable[ProductPart]:
        result = requests.get(os.path.join(self._base_url, 'product_parts'), params={
            'product': product_id,
        })
        result.raise_for_status()
        return [ProductPart(**part) for part in result.json()]

    def get_products(self) -> Iterable[Product]:
        result = requests.get(os.path.join(self._base_url, 'products'))
        result.raise_for_status()
        return [Product(**product) for product in result.json()]


def create_app(url: str = None) -> Union[Application, ApplicationProxy]:
    return ApplicationProxy(url) if url \
        else Application('sqlite+pysqlite:///:memory:')


def main() -> None:
    catalog = create_app('http://localhost:8080')
    product = select_product(catalog.get_products())
    parts = catalog.get_product_parts(product.id)
    options = select_options(parts, catalog.get_part_options)
    display_order_summary(
        product,
        parts,
        options,
        catalog.calculate_price(options))


def select_product(products: Iterable[Product]) -> Product:
    return select_elem(products, 'product')


def select_options(
        parts: Iterable[ProductPart],
        get_options: GetPartOptionsFunc) -> Iterable[PartOption]:
    selected = []
    for part in parts:
        selected.append(select_elem(
            get_options(part.id, selected),
            part.description.lower()))
    return selected


def select_elem(elems: Iterable, type_):
    elems = list(elems)
    for i, elem in enumerate(elems):
        print(f'{i + 1}: {elem.description}')
    while True:
        selected = input(f'Select {type_}: ')
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
