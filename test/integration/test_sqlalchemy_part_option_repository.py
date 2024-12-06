from unittest import TestCase

from sqlalchemy import create_engine

from catalog.domain import Description, PartOption
from catalog.sqlalchemy_infra import create_models, \
    SqlAlchemyPartOptionRepository
from .init_part_option_repository import init_part_option_repository


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
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], option_ids)

        options = [self._repo.get(id_) for id_ in option_ids]
        self.assertEqual(
            [
                PartOption(1, 1, Description('Full-suspension'), 130, True),
                PartOption(2, 1, Description('Diamond'), 100, True),
                PartOption(3, 1, Description('Step-through'), 90, True),
                PartOption(4, 2, Description('Matte'), 50, True),
                PartOption(5, 2, Description('Shiny'), 30, True),
                PartOption(6, 3, Description('Road wheels'), 80, True),
                PartOption(7, 3, Description('Mountain wheels'), 90, True),
                PartOption(8, 3, Description('Fat bike wheels'), 100, True),
                PartOption(9, 4, Description('Red'), 20, True),
                PartOption(10, 4, Description('Black'), 25, True),
                PartOption(11, 4, Description('Blue'), 20, True),
                PartOption(12, 5, Description('Single-speed chain'), 43, True),
                PartOption(13, 5, Description('8-speed chain'), 90, False),
            ],
            options)

    def test_get_options_for_part(self):
        self.assertEqual([4, 5], self._repo.list(2))

    def test_get_options_for_invalid_part(self):
        self.assertEqual([], self._repo.list(6))

    def test_get_invalid_option(self):
        self.assertIsNone(self._repo.get(14))

    def test_list_incompatibilities(self):
        self.assertEqual([7], list(self._repo.list_incompatibilities(2)))
        self.assertEqual([7], list(self._repo.list_incompatibilities(3)))
        self.assertEqual([9], list(self._repo.list_incompatibilities(8)))

        # Check if it can return the incompatibilities in the reverse order
        self.assertEqual([2, 3], list(self._repo.list_incompatibilities(7)))
        self.assertEqual([8], list(self._repo.list_incompatibilities(9)))

    def test_get_incompatibilities_for_invalid_option(self):
        self.assertEqual([], list(self._repo.list_incompatibilities(1)))

    def test_get_price_modifiers(self):
        depending_options = self._repo.list_depending_options(2)
        self.assertEqual([2], depending_options)

        price_coefs = [self._repo.get_depending_option_price_coef(2, id_)
                       for id_ in depending_options]
        self.assertEqual([0.7], price_coefs)

    def test_get_price_modifiers_for_invalid_option(self):
        self.assertEqual([], self._repo.list_depending_options(1))
        self.assertEqual(1, self._repo.get_depending_option_price_coef(1, 2))
