import logging
from unittest import TestCase

from catalog.application import TotalPriceAction
from catalog.domain import Money, PartOption
from .mock_part_option_repository import MockPartOptionRepository


class TestTotalPriceAction(TestCase):
    def setUp(self):
        self.repo = MockPartOptionRepository()
        self.total_price = TotalPriceAction(self.repo, logging.getLogger())

    def test_prices_witout_modifiers(self):
        self.assertEqual(
            Money(303),
            self.total_price([
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
            self.total_price([
                self.find_option('Diamond'),
                self.find_option('Matte'),
                self.find_option('Road wheels'),
                self.find_option('Blue'),
                self.find_option('Single-speed chain'),
            ])
        )

    def find_option(self, description: str) -> PartOption:
        return [self.repo.get(elem) for elem in self.repo.list()
                if str(self.repo.get(elem).description) == description][0]
