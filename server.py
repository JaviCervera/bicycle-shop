import json
from typing import Iterable

import cherrypy
import cherrypy_cors

from catalog.domain import PartOption, PartOptionRepository
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
            return json.dumps([product.__dict__ for product in app.get_products()])

    @cherrypy.expose
    def product_parts(self, product: str) -> str:
        with self.app() as app:
            return json.dumps([part.__dict__
                               for part in app.get_product_parts(int(product))])

    @cherrypy.expose
    def part_options(self, product_part: str, selected_options='') -> str:
        with self.app() as app:
            return json.dumps(
                [opt.__dict__ for opt in app.get_part_options(
                    int(product_part),
                    self.parse_options(selected_options, app.option_repo))])

    @cherrypy.expose
    def price(self, selected_options: str) -> str:
        with self.app() as app:
            selected = self.parse_options(selected_options, app.option_repo)
            return json.dumps({
                'price': app.calculate_price(selected)
            })

    @staticmethod
    def parse_options(options: str, repo: PartOptionRepository) -> Iterable[PartOption]:
        return [repo.get(int(opt.strip())) for opt in options.split(',')] if options else []

    @staticmethod
    def app() -> Application:
        app = Application('sqlite+pysqlite:///:memory:', True)
        init_product_repository(app.product_repo)
        init_product_part_repository(app.part_repo)
        init_part_option_repository(app.option_repo)
        return app

if __name__ == '__main__':
    cherrypy_cors.install()
    cherrypy.quickstart(Server())
