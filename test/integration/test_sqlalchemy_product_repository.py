from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from catalog.domain import Name, Product, ProductId
from catalog.infrastructure import create_models, SqlAlchemyProductRepository
from catalog.infrastructure.init_product_reposity \
    import init_product_repository


class TestSqlAlchemyProductRepository(TestCase):
    def setUp(self):
        engine = create_engine('sqlite+pysqlite:///:memory:')
        create_models(engine)
        self.session = Session(engine)
        self.repo = SqlAlchemyProductRepository(self.session)
        init_product_repository(self.repo)
        self.session.commit()


    def tearDown(self):
        self.session.close()

    def test_get_products(self):
        product_ids = self.repo.list()
        self.assertEqual([ProductId(1)], product_ids)

        products = [self.repo.get(id_) for id_ in product_ids]
        self.assertEqual(
            [Product(ProductId(1), Name('Bicycles'))],
            products)

    def test_get_invalid_product(self):
        self.assertIsNone(self.repo.get(ProductId(2)))
