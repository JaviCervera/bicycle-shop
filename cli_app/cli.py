from argparse import ArgumentParser
from typing import Callable, Iterable, List, Optional, Sequence

from catalog.domain import Description, Money, PartOption, Product, \
    ProductPart, ProductPartId

GetPartOptionsFunc = \
    Callable[[ProductPartId, Iterable[PartOption]], Iterable[PartOption]]


def server_url() -> Optional[str]:
    """ Retrieves the server URL from the command line args. """
    parser = ArgumentParser()
    parser.add_argument('-u', '--url')
    return parser.parse_args().url


def print_welcome_message(url: Optional[str]) -> None:
    """
    Prints a welcome message, indicating if running in monolithic mode
    (with the backend bundled in the application) or against a server.
    """
    print('Welcome to Markus Sports Equipment Store!')
    if url:
        print(f'Running on {url}')
    else:
        print('Running in monolithic mode')
    print()


def select_product(products: Iterable[Product]) -> Product:
    """
    Displays a list with all passed product and returns
    the one selected by the user.
    """
    sel_index = _select_elem([p.description for p in products], [], 'product')
    return list(products)[sel_index]


def select_options(
        parts: Iterable[ProductPart],
        get_options: GetPartOptionsFunc) -> Iterable[PartOption]:
    """
    Displays a list with all available options for each part passed
    and returns the ones selected by the user.

    :param parts: The parts to select options from.
    :param get_options: Callable that returns the options for the given part.
    :return: All options selected.
    """
    selected: List[PartOption] = []
    for part in parts:
        options = list(get_options(part.id, selected))
        sel_option = _select_elem(
            [opt.description for opt in options],
            [opt.price for opt in options],
            str(part.description).lower())
        selected.append(options[sel_option])
    return selected


def _select_elem(
        names: Sequence[Description],
        prices: Sequence[Money], type_: str) -> int:
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
        price: Money) -> None:
    """
    Displays a summary of the selected parts for the purchased product,
    with the final price.

    :param product: The selected product.
    :param parts: All parts for the given product.
    :param selected: The selected options for the parts.
    :param price: The total price.
    """
    print()
    print(f'Your {product.description} order:')
    for opt in selected:
        part = [part for part in parts if part.id == opt.part_id][0]
        print(f'* {part.description}: {opt.description}')
    print()
    print(f'Total price: {price} EUR')
