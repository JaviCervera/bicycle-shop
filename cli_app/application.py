import logging
import os
from typing import Iterable, Optional, Self, Union

import requests

from catalog.domain import Money, PartOption, Product, ProductId, \
    ProductPart, ProductPartId
from catalog.infrastructure import Application
from catalog.infrastructure.schemas import PartOptionSchema, ProductPartSchema, ProductSchema
from test.integration.init_part_option_repository \
    import init_part_option_repository
from test.integration.init_product_part_repository \
    import init_product_part_repository
from test.integration.init_product_reposity import init_product_repository


class ApplicationProxy:
    def __init__(self, url: str) -> None:
        self._base_url = url

    def part_options(
            self,
            part_id: ProductPartId,
            selected: Iterable[PartOption]) -> Iterable[PartOption]:
        result = requests.get(os.path.join(self._base_url, 'part_options'), params={
            'product_part': str(part_id),
            'selected_options': self._join_options(selected),
        })
        result.raise_for_status()
        return PartOptionSchema().load(result.json(), many=True)

    @staticmethod
    def _join_options(options: Iterable[PartOption]) -> str:
        return ','.join([str(opt.id) for opt in options])

    def product_parts(self, product_id: ProductId) -> Iterable[ProductPart]:
        result = requests.get(os.path.join(self._base_url, 'product_parts'), params={
            'product': int(product_id),
        })
        result.raise_for_status()
        return ProductPartSchema().load(result.json(), many=True)

    def products(self) -> Iterable[Product]:
        result = requests.get(os.path.join(self._base_url, 'products'))
        result.raise_for_status()
        return ProductSchema().load(result.json(), many=True)

    def total_price(self, selected: Iterable[PartOption]) -> Money:
        result = requests.get(os.path.join(self._base_url, 'price'), params={
            'selected_options': self._join_options(selected),
        })
        result.raise_for_status()
        return Money(float(result.json()['price']))

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args) -> None:
        pass


def create_app(
        url: Optional[str] = None) -> Union[Application, ApplicationProxy]:
    if url:
        return ApplicationProxy(url)
    else:
        app = Application('sqlite+pysqlite:///:memory:', logging.getLogger())
        init_product_repository(app.product_repo)
        init_product_part_repository(app.part_repo)
        init_part_option_repository(app.option_repo)
        return app
