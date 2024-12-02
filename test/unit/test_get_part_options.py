from unittest import TestCase

from catalog.application import GetPartOptionsCommand
from catalog.domain import PartOption, ProductPart
from .mock_part_option_repository import MockPartOptionRepository
from .mock_product_part_repository import MockProductPartRepository

class TestGetPartOptionsCommand(TestCase):
  def setUp(self):
    self.part_repo = MockProductPartRepository()
    self.option_repo = MockPartOptionRepository()
    self.get_part_options = GetPartOptionsCommand(self.option_repo)

  def test_only_returns_options_compatible_with_selection(self):
    self.assertEqual(
      [
        self.find_option('Full-suspension'),
        self.find_option('Diamond'),
        self.find_option('Step-through'),
      ],
      self.get_part_options(self.find_part('Frame type'), [])
    )

    self.assertEqual(
      [
        self.find_option('Red'),
        self.find_option('Black'),
        self.find_option('Blue')
      ],
      self.get_part_options(self.find_part('Rim color'), [])
    )

    self.assertEqual(
      [self.find_option('Full-suspension')],
      self.get_part_options(
        self.find_part('Frame type'),
        [self.find_option('Mountain wheels')]
      )
    )

    self.assertEqual(
      [self.find_option('Black'), self.find_option('Blue')],
      self.get_part_options(
        self.find_part('Rim color'),
        [self.find_option('Fat bike wheels')]
      )
    )
  
  def test_only_returns_options_in_stock(self):
    self.assertEqual(
      [self.find_option('Single-speed chain')],
      self.get_part_options(
        self.find_part('Chain'),
        [
          self.find_option('Single-speed chain'),
          self.find_option('8-speed chain'),
        ]
      )
    )

  def find_part(self, description: str) -> ProductPart:
    return self.find_elem(self.part_repo, description)

  def find_option(self, description: str) -> PartOption:
    return self.find_elem(self.option_repo, description)
  
  @staticmethod
  def find_elem(repo, description: str):
    return [repo.get(elem) for elem in repo.list()
            if repo.get(elem).description == description][0]
