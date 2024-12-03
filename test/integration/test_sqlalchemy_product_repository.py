from unittest import TestCase

from sqlalchemy import create_engine

from catalog.domain import Product
from catalog.sqlalchemy_infra import create_models, SqlAlchemyProductRepository
from .init_product_reposity import init_product_repository


class TestSqlAlchemyProductRepository(TestCase):
    def setUp(self):
        engine = create_engine('sqlite+pysqlite:///:memory:')
        create_models(engine)
        self._repo = SqlAlchemyProductRepository(engine)
        init_product_repository(self._repo)

    def tearDown(self):
        self._repo.close()

    def test_get_products(self):
        product_ids = self._repo.list()
        self.assertEqual([1], product_ids)

        products = [self._repo.get(id_) for id_ in product_ids]
        self.assertEqual([Product(1, 'Bicycles')], products)

    def test_get_invalid_product(self):
        self.assertIsNone(self._repo.get(2))
