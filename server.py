import json
import logging
import sys
from typing import Iterable

import cherrypy  # type: ignore
import cherrypy_cors  # type: ignore

from catalog.domain import PartOption, PartOptionRepository, ProductId, \
    ProductPartId
from catalog.schemas import PartOptionSchema, ProductPartSchema, ProductSchema
from catalog.sqlalchemy_infra import Application
from test.integration.init_part_option_repository \
    import init_part_option_repository
from test.integration.init_product_part_repository \
    import init_product_part_repository
from test.integration.init_product_reposity import init_product_repository


class Server:
    @cherrypy.expose
    def products(self) -> str:
        with self.app() as app:
            return ProductSchema().dumps(app.products(), many=True)

    @cherrypy.expose
    def product_parts(self, product: str) -> str:
        with self.app() as app:
            parts = app.product_parts(ProductId(int(product)))
            return ProductPartSchema().dumps(parts, many=True)

    @cherrypy.expose
    def part_options(self, product_part: str, selected_options='') -> str:
        with self.app() as app:
            options = app.part_options(
                ProductPartId(int(product_part)),
                self.parse_options(selected_options, app.option_repo))
            return PartOptionSchema().dumps(options, many=True)

    @cherrypy.expose
    def price(self, selected_options: str) -> str:
        with self.app() as app:
            selected = self.parse_options(selected_options, app.option_repo)
            return json.dumps({
                'price': float(app.total_price(selected))
            })

    @staticmethod
    def parse_options(options: str, repo: PartOptionRepository) -> Iterable[PartOption]:
        if options:
            return [repo.get(int(opt.strip())) for opt in options.split(',')]  # type: ignore
        else:
            return []

    @staticmethod
    def app() -> Application:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        logger = logging.getLogger()
        app = Application('sqlite+pysqlite:///:memory:', logger)
        init_product_repository(app.product_repo)
        init_product_part_repository(app.part_repo)
        init_part_option_repository(app.option_repo)
        return app

if __name__ == '__main__':
    cherrypy_cors.install()
    cherrypy.quickstart(Server())
