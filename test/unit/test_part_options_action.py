from unittest import TestCase

from catalog.application import PartOptionsAction
from catalog.domain import PartOption, ProductPartId
from .mock_part_option_repository import MockPartOptionRepository
from .mock_product_part_repository import MockProductPartRepository


class TestPartOptionsAction(TestCase):
    def setUp(self):
        self.part_repo = MockProductPartRepository()
        self.option_repo = MockPartOptionRepository()
        self.part_options = PartOptionsAction(self.option_repo)

    def test_only_returns_options_compatible_with_selection(self):
        self.assertEqual(
            [
                self.find_option('Full-suspension'),
                self.find_option('Diamond'),
                self.find_option('Step-through'),
            ],
            self.part_options(self.find_part('Frame type'), [])
        )

        self.assertEqual(
            [
                self.find_option('Red'),
                self.find_option('Black'),
                self.find_option('Blue')
            ],
            self.part_options(self.find_part('Rim color'), [])
        )

        self.assertEqual(
            [self.find_option('Full-suspension')],
            self.part_options(
                self.find_part('Frame type'),
                [self.find_option('Mountain wheels')]
            )
        )

        self.assertEqual(
            [self.find_option('Black'), self.find_option('Blue')],
            self.part_options(
                self.find_part('Rim color'),
                [self.find_option('Fat bike wheels')]
            )
        )

    def test_only_returns_options_in_stock(self):
        self.assertEqual(
            [self.find_option('Single-speed chain')],
            self.part_options(
                self.find_part('Chain'),
                [
                    self.find_option('Single-speed chain'),
                    self.find_option('8-speed chain'),
                ]
            )
        )

    def find_part(self, name: str) -> ProductPartId:
        return self.find_elem(self.part_repo, name).id

    def find_option(self, name: str) -> PartOption:
        return self.find_elem(self.option_repo, name)

    @staticmethod
    def find_elem(repo, name: str):
        return [repo.get(elem) for elem in repo.list()
                if str(repo.get(elem).name) == name][0]
