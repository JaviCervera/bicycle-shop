from unittest import TestCase

from sqlalchemy import create_engine

from catalog.domain import Money, Name, PartOption, PartOptionId, \
    ProductPartId, Units
from catalog.infrastructure import create_models, \
    SqlAlchemyPartOptionRepository
from catalog.infrastructure.init_part_option_repository import init_part_option_repository


class TestSqlAlchemyPartOptionRepository(TestCase):
    def setUp(self):
        engine = create_engine('sqlite+pysqlite:///:memory:')
        create_models(engine)
        self._repo = SqlAlchemyPartOptionRepository(engine)
        init_part_option_repository(self._repo)

    def tearDown(self):
        self._repo.close()

    def test_get_options(self):
        option_ids = self._repo.list()
        self.assertEqual(
            [
                PartOptionId(1),
                PartOptionId(2),
                PartOptionId(3),
                PartOptionId(4),
                PartOptionId(5),
                PartOptionId(6),
                PartOptionId(7),
                PartOptionId(8),
                PartOptionId(9),
                PartOptionId(10),
                PartOptionId(11),
                PartOptionId(12),
                PartOptionId(13),
            ],
            option_ids)

        options = [self._repo.get(id_) for id_ in option_ids]
        self.assertEqual(
            [
                PartOption(
                    PartOptionId(1),
                    ProductPartId(1),
                    Name('Full-suspension'),
                    Money(130),
                    Units(10)),
                PartOption(
                    PartOptionId(2),
                    ProductPartId(1),
                    Name('Diamond'),
                    Money(100),
                    Units(7)),
                PartOption(
                    PartOptionId(3),
                    ProductPartId(1),
                    Name('Step-through'),
                    Money(90),
                    Units(3)),
                PartOption(
                    PartOptionId(4),
                    ProductPartId(2),
                    Name('Matte'),
                    Money(50),
                    Units(5)),
                PartOption(
                    PartOptionId(5),
                    ProductPartId(2),
                    Name('Shiny'),
                    Money(30),
                    Units(7)),
                PartOption(
                    PartOptionId(6),
                    ProductPartId(3),
                    Name('Road wheels'),
                    Money(80),
                    Units(24)),
                PartOption(
                    PartOptionId(7),
                    ProductPartId(3),
                    Name('Mountain wheels'),
                    Money(90),
                    Units(1)),
                PartOption(
                    PartOptionId(8),
                    ProductPartId(3),
                    Name('Fat bike wheels'),
                    Money(100),
                    Units(15)),
                PartOption(
                    PartOptionId(9),
                    ProductPartId(4),
                    Name('Red'),
                    Money(20),
                    Units(20)),
                PartOption(
                    PartOptionId(10),
                    ProductPartId(4),
                    Name('Black'),
                    Money(25),
                    Units(32)),
                PartOption(
                    PartOptionId(11),
                    ProductPartId(4),
                    Name('Blue'),
                    Money(20),
                    Units(11)),
                PartOption(
                    PartOptionId(12),
                    ProductPartId(5),
                    Name('Single-speed chain'),
                    Money(43),
                    Units(6)),
                PartOption(
                    PartOptionId(13),
                    ProductPartId(5),
                    Name('8-speed chain'),
                    Money(90),
                    Units(0)),
            ],
            options)

    def test_get_options_for_part(self):
        self.assertEqual(
            [PartOptionId(4), PartOptionId(5)],
            self._repo.list(ProductPartId(2)))

    def test_get_options_for_invalid_part(self):
        self.assertEqual([], self._repo.list(ProductPartId(6)))

    def test_get_invalid_option(self):
        self.assertIsNone(self._repo.get(PartOptionId(14)))

    def test_list_incompatibilities(self):
        self.assertEqual(
            [PartOptionId(7)],
            list(self._repo.list_incompatibilities(PartOptionId(2))))
        self.assertEqual(
            [PartOptionId(7)],
            list(self._repo.list_incompatibilities(PartOptionId(3))))
        self.assertEqual(
            [PartOptionId(9)],
            list(self._repo.list_incompatibilities(PartOptionId(8))))

        # Check if it can return the incompatibilities in the reverse order
        self.assertEqual(
            [PartOptionId(2), PartOptionId(3)],
            list(self._repo.list_incompatibilities(PartOptionId(7))))
        self.assertEqual(
            [PartOptionId(8)],
            list(self._repo.list_incompatibilities(PartOptionId(9))))

    def test_get_incompatibilities_for_invalid_option(self):
        self.assertEqual(
            [],
            list(self._repo.list_incompatibilities(PartOptionId(1))))

    def test_get_price_modifiers(self):
        depending_options = self._repo.list_depending_options(ProductPartId(2))
        self.assertEqual([PartOptionId(2)], depending_options)

        price_coefs = [
            self._repo.get_depending_option_price_coef(ProductPartId(2), id_)
            for id_ in depending_options]
        self.assertEqual([0.7], price_coefs)

    def test_get_price_modifiers_for_invalid_option(self):
        self.assertEqual(
            [],
            self._repo.list_depending_options(ProductPartId(1)))
        self.assertEqual(
            1,
            self._repo.get_depending_option_price_coef(
                ProductPartId(1),
                PartOptionId(2)))
