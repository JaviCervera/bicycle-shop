from unittest import TestCase

from sqlalchemy import create_engine

from catalog.domain import Name, Product, ProductId
from catalog.infrastructure import create_models, SqlAlchemyProductRepository
from catalog.infrastructure.init_product_reposity import init_product_repository


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
        self.assertEqual([ProductId(1)], product_ids)

        products = [self._repo.get(id_) for id_ in product_ids]
        self.assertEqual(
            [Product(ProductId(1), Name('Bicycles'))],
            products)

    def test_get_invalid_product(self):
        self.assertIsNone(self._repo.get(ProductId(2)))
