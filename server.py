import json
from typing import Iterable, Self

import cherrypy
import cherrypy_cors

from sqlalchemy import create_engine

from catalog.application import CalculatePriceCommand, GetPartOptionsCommand, \
    GetProductPartsCommand, GetProductsCommand
from catalog.domain import PartOption, PartOptionRepository
from catalog.sqlalchemy_infra import create_models, \
    SqlAlchemyPartOptionRepository, SqlAlchemyProductPartRepository, \
    SqlAlchemyProductRepository
from test.integration.init_part_option_repository \
    import init_part_option_repository
from test.integration.init_product_part_repository \
    import init_product_part_repository
from test.integration.init_product_reposity import init_product_repository


class Application:
    def __init__(self):
        engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)
        create_models(engine)
        self.product_repo = SqlAlchemyProductRepository(engine)
        self.part_repo = SqlAlchemyProductPartRepository(engine)
        self.option_repo = SqlAlchemyPartOptionRepository(engine)
        init_product_repository(self.product_repo)
        init_product_part_repository(self.part_repo)
        init_part_option_repository(self.option_repo)
        self.get_products = GetProductsCommand(self.product_repo)
        self.get_product_parts = GetProductPartsCommand(self.part_repo)
        self.get_part_options = GetPartOptionsCommand(self.option_repo)
        self.calculate_price = CalculatePriceCommand(self.option_repo)

    def __enter__(self) -> Self:
        self.product_repo.__enter__()
        self.part_repo.__enter__()
        self.option_repo.__enter__()
        return self

    def __exit__(self, *args) -> None:
        self.product_repo.__exit__()
        self.part_repo.__exit__()
        self.option_repo.__exit__()


class Server:
    @cherrypy.expose
    def products(self) -> str:
        with Application() as app:
            return json.dumps([product.__dict__ for product in app.get_products()])

    @cherrypy.expose
    def product_parts(self, product: str) -> str:
        with Application() as app:
            return json.dumps([part.__dict__
                               for part in app.get_product_parts(int(product))])

    @cherrypy.expose
    def part_options(self, product_part: str, selected_options='') -> str:
        with Application() as app:
            return json.dumps(
                [opt.__dict__ for opt in app.get_part_options(
                    int(product_part),
                    self._parse_options(selected_options, app.option_repo))])

    @cherrypy.expose
    def price(self, selected_options: str) -> str:
        with Application() as app:
            selected = self._parse_options(selected_options, app.option_repo)
            return json.dumps({
                'price': app.calculate_price(selected)
            })

    @staticmethod
    def _parse_options(options: str, repo: PartOptionRepository) -> Iterable[PartOption]:
        return [repo.get(int(opt.strip())) for opt in options.split(',')] if options else []


if __name__ == '__main__':
    cherrypy_cors.install()
    cherrypy.quickstart(Server())
