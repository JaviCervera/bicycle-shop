from unittest import TestCase

from sqlalchemy import create_engine

from catalog.domain import Description, Money, PartOption, PartOptionId, \
    ProductPartId
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
                    Description('Full-suspension'),
                    Money(130),
                    True),
                PartOption(
                    PartOptionId(2),
                    ProductPartId(1),
                    Description('Diamond'),
                    Money(100),
                    True),
                PartOption(
                    PartOptionId(3),
                    ProductPartId(1),
                    Description('Step-through'),
                    Money(90),
                    True),
                PartOption(
                    PartOptionId(4),
                    ProductPartId(2),
                    Description('Matte'),
                    Money(50),
                    True),
                PartOption(
                    PartOptionId(5),
                    ProductPartId(2),
                    Description('Shiny'),
                    Money(30),
                    True),
                PartOption(
                    PartOptionId(6),
                    ProductPartId(3),
                    Description('Road wheels'),
                    Money(80),
                    True),
                PartOption(
                    PartOptionId(7),
                    ProductPartId(3),
                    Description('Mountain wheels'),
                    Money(90),
                    True),
                PartOption(
                    PartOptionId(8),
                    ProductPartId(3),
                    Description('Fat bike wheels'),
                    Money(100),
                    True),
                PartOption(
                    PartOptionId(9),
                    ProductPartId(4),
                    Description('Red'),
                    Money(20),
                    True),
                PartOption(
                    PartOptionId(10),
                    ProductPartId(4),
                    Description('Black'),
                    Money(25),
                    True),
                PartOption(
                    PartOptionId(11),
                    ProductPartId(4),
                    Description('Blue'),
                    Money(20),
                    True),
                PartOption(
                    PartOptionId(12),
                    ProductPartId(5),
                    Description('Single-speed chain'),
                    Money(43),
                    True),
                PartOption(
                    PartOptionId(13),
                    ProductPartId(5),
                    Description('8-speed chain'),
                    Money(90),
                    False),
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
