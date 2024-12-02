from unittest import TestCase

from catalog.domain import PartOption, PartOptionFilter, ProductPart
from catalog.test_infrastructure import TestPartOptionRepository, \
  TestProductPartRepository

class TestPartOptionFilter(TestCase):
  def setUp(self):
    self.filter = PartOptionFilter(TestPartOptionRepository())

  def test_only_returns_options_compatible_with_selection(self):
    self.assertEqual(
      [
        self.find_option('Full-suspension'),
        self.find_option('Diamond'),
        self.find_option('Step-through'),
      ],
      self.filter.compatible(self.find_part('Frame type'), [])
    )

    self.assertEqual(
      [
        self.find_option('Red'),
        self.find_option('Black'),
        self.find_option('Blue')
      ],
      self.filter.compatible(self.find_part('Rim color'), [])
    )

    self.assertEqual(
      [self.find_option('Full-suspension')],
      self.filter.compatible(
        self.find_part('Frame type'),
        [self.find_option('Mountain wheels')]
      )
    )

    self.assertEqual(
      [self.find_option('Black'), self.find_option('Blue')],
      self.filter.compatible(
        self.find_part('Rim color'),
        [self.find_option('Fat bike wheels')]
      )
    )
  
  def test_only_returns_options_in_stock(self):
    self.assertEqual(
      [self.find_option('Single-speed chain')],
      self.filter.in_stock([
        self.find_option('Single-speed chain'),
        self.find_option('8-speed chain'),
      ])
    )

  def find_part(self, description: str) -> ProductPart:
    return self.find_elem(TestProductPartRepository(), description)

  def find_option(self, description: str) -> PartOption:
    return self.find_elem(TestPartOptionRepository(), description)
  
  @staticmethod
  def find_elem(repo, description: str):
    return [repo.get(elem) for elem in repo.list()
            if repo.get(elem).description == description][0]
