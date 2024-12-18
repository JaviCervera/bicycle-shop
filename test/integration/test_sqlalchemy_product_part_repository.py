from unittest import TestCase

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from catalog.domain import Name, ProductId, ProductPart, ProductPartId
from catalog.infrastructure import create_models, \
    SqlAlchemyProductPartRepository
from catalog.infrastructure.init_product_part_repository \
    import init_product_part_repository


class TestSqlAlchemyProductPartRepository(TestCase):
    def setUp(self):
        engine = create_engine('sqlite+pysqlite:///:memory:')
        create_models(engine)
        self.session = Session(engine)
        self.repo = SqlAlchemyProductPartRepository(self.session)
        init_product_part_repository(self.repo)
        self.session.commit()

    def tearDown(self):
        self.session.close()

    def test_get_parts(self):
        part_ids = self.repo.list()
        self.assertEqual([1, 2, 3, 4, 5], part_ids)

        parts = [self.repo.get(id_) for id_ in part_ids]
        self.assertEqual(
            [
                ProductPart(
                    ProductPartId(1),
                    ProductId(1),
                    Name('Frame type')),
                ProductPart(
                    ProductPartId(2),
                    ProductId(1),
                    Name('Frame finish')),
                ProductPart(
                    ProductPartId(3),
                    ProductId(1),
                    Name('Wheels')),
                ProductPart(
                    ProductPartId(4),
                    ProductId(1),
                    Name('Rim color')),
                ProductPart(
                    ProductPartId(5),
                    ProductId(1),
                    Name('Chain')),
            ],
            parts)

    def test_get_parts_for_product(self):
        self.assertEqual([1, 2, 3, 4, 5], self.repo.list(ProductId(1)))

    def test_get_parts_for_invalid_product(self):
        self.assertEqual([], self.repo.list(ProductId(2)))

    def test_get_invalid_part(self):
        self.assertIsNone(self.repo.get(ProductPartId(6)))
