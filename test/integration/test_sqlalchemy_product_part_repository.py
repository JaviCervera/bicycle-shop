from unittest import TestCase

from sqlalchemy import create_engine

from catalog.domain import ProductPart
from catalog.sqlalchemy_infra import create_models, SqlAlchemyProductPartRepository
from .init_product_part_repository import init_product_part_repository


class TestSqlAlchemyProductPartRepository(TestCase):
    def setUp(self):
        engine = create_engine('sqlite+pysqlite:///:memory:')
        create_models(engine)
        self._repo = SqlAlchemyProductPartRepository(engine)
        init_product_part_repository(self._repo)

    def tearDown(self):
        self._repo.close()

    def test_get_parts(self):
        part_ids = self._repo.list()
        self.assertEqual([1, 2, 3, 4, 5], part_ids)

        parts = [self._repo.get(id_) for id_ in part_ids]
        self.assertEqual(
            [
                ProductPart(1, 1, 'Frame type'),
                ProductPart(2, 1, 'Frame finish'),
                ProductPart(3, 1, 'Wheels'),
                ProductPart(4, 1, 'Rim color'),
                ProductPart(5, 1, 'Chain'),
            ],
            parts)

    def test_get_parts_for_product(self):
        self.assertEqual([1, 2, 3, 4, 5], self._repo.list(1))

    def test_get_parts_for_invalid_product(self):
        self.assertEqual([], self._repo.list(2))

    def test_get_invalid_part(self):
        self.assertIsNone(self._repo.get(6))
