from unittest import TestCase

from catalog.domain import PartOption, PriceCalculator
from catalog.test_infrastructure import TestPartOptionRepository


class TestPriceCalculator(TestCase):
  def test_prices_witout_modifiers(self):
    self.assertEqual(
      303,
      PriceCalculator(TestPartOptionRepository())([
        self.find_option('Full-suspension'),
        self.find_option('Shiny'),
        self.find_option('Road wheels'),
        self.find_option('Blue'),
        self.find_option('Single-speed chain'),
      ])
    )
  
  def test_prices_with_modifiers(self):
    # Without the modifier, it would be 293
    self.assertEqual(
      278,
      PriceCalculator(TestPartOptionRepository())([
        self.find_option('Diamond'),
        self.find_option('Matte'),
        self.find_option('Road wheels'),
        self.find_option('Blue'),
        self.find_option('Single-speed chain'),
      ])
    )

  @staticmethod
  def find_option(description: str) -> PartOption:
    repo = TestPartOptionRepository()
    return [repo.get(elem) for elem in repo.list()
            if repo.get(elem).description == description][0]
