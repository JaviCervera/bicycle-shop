import logging
from argparse import ArgumentParser
from typing import Callable, Iterable, List, Optional, Sequence

from catalog.domain import PartOption, Product, ProductPart, ProductPartId
from cli_app import create_app

GetPartOptionsFunc = \
    Callable[[ProductPartId, Iterable[PartOption]], Iterable[PartOption]]


def main() -> None:
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    url = server_url()
    print_welcome_message(url)
    with create_app(url) as app:
        product = select_product(app.products())
        parts = app.product_parts(product.id)
        options = select_options(parts, app.part_options)
        display_order_summary(
            product,
            parts,
            options,
            app.total_price(options))


def server_url() -> Optional[str]:
    parser = ArgumentParser()
    parser.add_argument('-u', '--url')
    return parser.parse_args().url


def print_welcome_message(url: Optional[str]) -> None:
    print('Welcome to Markus Sports Equipment Store!')
    if url:
        print(f'Running on {url}')
    else:
        print('Running in local mode')
    print()


def select_product(products: Iterable[Product]) -> Product:
    sel_index = select_elem([p.description for p in products], [], 'product')
    return list(products)[sel_index]


def select_options(
        parts: Iterable[ProductPart],
        get_options: GetPartOptionsFunc) -> Iterable[PartOption]:
    selected: List[PartOption] = []
    for part in parts:
        options = list(get_options(part.id, selected))
        sel_option = select_elem(
            [opt.description for opt in options],
            [opt.price for opt in options],
            part.description.lower())
        selected.append(options[sel_option])
    return selected


def select_elem(names: Sequence[str], prices: Sequence[float], type_: str) -> int:
    print(f'Select {type_}:')
    for i in range(len(names)):
        price_str = f' - {prices[i]} EUR' if len(prices) > i else ''
        print(f'{i + 1}: {names[i]}{price_str}')
    while True:
        selected = input('> ')
        if not selected.isdigit() \
                or int(selected) not in range(1, len(names) + 1):
            print(f'Please enter a number between 1 and {len(names)}')
        else:
            print()
            return int(selected) - 1


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
    print(f'Total price: {price} EUR')


if __name__ == '__main__':
    main()
