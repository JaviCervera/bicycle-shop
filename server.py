"""
Marcus Sports Equipment Store - Simple web server
=================================================

Please check README.md or the header of main.py file
for instructions.
"""

import json
import logging
import sys
from typing import Iterable

import cherrypy  # type: ignore
import cherrypy_cors  # type: ignore

from catalog.domain import PartOption, PartOptionRepository, ProductId, \
    ProductPartId
from catalog.infrastructure import Catalog
from catalog.infrastructure.schemas import PartOptionSchema, ProductPartSchema, ProductSchema
from catalog.infrastructure.init_part_option_repository \
    import init_part_option_repository
from catalog.infrastructure.init_product_part_repository \
    import init_product_part_repository
from catalog.infrastructure.init_product_reposity import init_product_repository


class Server:
    @cherrypy.expose
    def products(self) -> str:
        with self.catalog() as app:
            return ProductSchema().dumps(app.products(), many=True)

    @cherrypy.expose
    def product_parts(self, product: str) -> str:
        with self.catalog() as app:
            parts = app.product_parts(ProductId(int(product)))
            return ProductPartSchema().dumps(parts, many=True)

    @cherrypy.expose
    def part_options(self, product_part: str, selected_options='') -> str:
        with self.catalog() as app:
            options = app.part_options(
                ProductPartId(int(product_part)),
                self.parse_options(selected_options, app.option_repo))
            return PartOptionSchema().dumps(options, many=True)

    @cherrypy.expose
    def part_options_price(self, selected_options: str) -> str:
        with self.catalog() as catalog:
            selected = self.parse_options(
                selected_options,
                catalog.option_repo)
            return json.dumps({
                'price': float(catalog.part_options_price(selected))
            })

    @staticmethod
    def parse_options(options: str, repo: PartOptionRepository) -> Iterable[PartOption]:
        if options:
            return [repo.get(int(opt.strip())) for opt in options.split(',')]  # type: ignore
        else:
            return []

    @staticmethod
    def catalog() -> Catalog:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        catalog = Catalog('sqlite+pysqlite:///:memory:', True)
        init_product_repository(catalog.product_repo)
        init_product_part_repository(catalog.part_repo)
        init_part_option_repository(catalog.option_repo)
        catalog.session.commit()
        return catalog

if __name__ == '__main__':
    cherrypy_cors.install()
    cherrypy.quickstart(Server(), '/catalog')
