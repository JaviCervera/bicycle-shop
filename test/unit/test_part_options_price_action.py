from unittest import TestCase

from catalog.application import PartOptionsPriceAction
from catalog.domain import Money, PartOption
from .mock_part_option_repository import MockPartOptionRepository


class TestTotalPriceAction(TestCase):
    def setUp(self):
        self.repo = MockPartOptionRepository()
        self.part_options_price = PartOptionsPriceAction(self.repo)

    def test_prices_witout_modifiers(self):
        self.assertEqual(
            Money(303),
            self.part_options_price([
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
            Money(278),
            self.part_options_price([
                self.find_option('Diamond'),
                self.find_option('Matte'),
                self.find_option('Road wheels'),
                self.find_option('Blue'),
                self.find_option('Single-speed chain'),
            ])
        )

    def find_option(self, name: str) -> PartOption:
        return [self.repo.get(elem) for elem in self.repo.list()
                if str(self.repo.get(elem).name) == name][0]
