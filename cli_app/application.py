import os
from typing import Iterable, Optional, Self, Union

import requests

from catalog.domain import PartOption, Product, ProductId, ProductPart, \
    ProductPartId
from catalog.sqlalchemy_infra import Application

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
            'product_part': str(part_id),
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

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args) -> None:
        pass


def create_app(
        url: Optional[str] = None) -> Union[Application, ApplicationProxy]:
    return ApplicationProxy(url) if url \
        else Application('sqlite+pysqlite:///:memory:')
