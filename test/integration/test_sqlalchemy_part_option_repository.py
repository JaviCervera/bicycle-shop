from unittest import TestCase

from sqlalchemy import create_engine

from catalog.domain import PartOption
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

    options = [self._repo.get(id) for id in option_ids]
    self.assertEqual(
      [
        PartOption(1, 1, 'Full-suspension', 130, True),
        PartOption(2, 1, 'Diamond', 100, True),
        PartOption(3, 1, 'Step-through', 90, True),
        PartOption(4, 2, 'Matte', 50, True),
        PartOption(5, 2, 'Shiny', 30, True),
        PartOption(6, 3, 'Road wheels', 80, True),
        PartOption(7, 3, 'Mountain wheels', 90, True),
        PartOption(8, 3, 'Fat bike wheels', 100, True),
        PartOption(9, 4, 'Red', 20, True),
        PartOption(10, 4, 'Black', 25, True),
        PartOption(11, 4, 'Blue', 20, True),
        PartOption(12, 5, 'Single-speed chain', 43, True),
        PartOption(13, 5, '8-speed chain', 90, False),
      ],
      options)

  def test_get_options_for_part(self):
    self.assertEqual([4, 5], self._repo.list(2))

  def test_get_options_for_invalid_part(self):
    self.assertEqual([], self._repo.list(6))

  def test_get_invalid_option(self):
    self.assertIsNone(self._repo.get(14))
  
  def test_get_incompatibilities_for_option(self):
    self.assertEqual([7], self._repo.list_incompatibilies(2))
    self.assertEqual([7], self._repo.list_incompatibilies(3))
    self.assertEqual([9], self._repo.list_incompatibilies(8))

  def test_get_incompatibilities_for_invalid_option(self):
    self.assertEqual([], self._repo.list_incompatibilies(1))

  def test_get_price_modifiers(self):
    depending_options = self._repo.list_depending_options(2)
    self.assertEqual([2], depending_options)

    price_coefs = [self._repo.get_depending_option_price_coef(2, id)
                   for id in depending_options]
    self.assertEqual([0.7], price_coefs)
  
  def test_get_price_modifiers_for_invalid_option(self):
    self.assertEqual([], self._repo.list_depending_options(1))
    self.assertEqual(1, self._repo.get_depending_option_price_coef(1, 2))
