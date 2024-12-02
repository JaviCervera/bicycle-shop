from unittest import TestCase

from catalog.domain import PartOption, Product, ProductPart
from catalog.test_infrastructure import TestPartOptionRepository, \
  TestProductPartRepository, TestProductRepository

class TestDataModel(TestCase):
  def setUp(self):
    self.product_repo = TestProductRepository()
    self.part_repo = TestProductPartRepository()
    self.option_repo = TestPartOptionRepository()

  def test_get_products(self):
    product_ids = self.product_repo.list()
    self.assertEqual([1], product_ids)

    products = [self.product_repo.get(id) for id in product_ids]
    self.assertEqual([Product(1, 'Bicycles')], products)

  def test_get_invalid_product(self):
    self.assertIsNone(self.product_repo.get(2))

  def test_get_parts(self):
    part_ids = self.part_repo.list()
    self.assertEqual([1, 2, 3, 4, 5], part_ids)

    parts = [self.part_repo.get(id) for id in part_ids]
    self.assertEqual(
      [
        ProductPart(1, 1, 'Frame type'),
        ProductPart(2, 1, 'Frame finish'),
        ProductPart(3, 1, 'Wheels'),
        ProductPart(4, 1, 'Rim color'),
        ProductPart(5, 1, 'Chain'),
      ],
      parts)
  
  def test_get_parts_for_product(self):
    self.assertEqual([1, 2, 3, 4, 5], self.part_repo.list(1))
  
  def test_get_parts_for_invalid_product(self):
    self.assertEqual([], self.part_repo.list(2))
  
  def test_get_invalid_part(self):
    self.assertIsNone(self.part_repo.get(6))

  def test_get_options(self):
    option_ids = self.option_repo.list()
    self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], option_ids)

    options = [self.option_repo.get(id) for id in option_ids]
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
    self.assertEqual([4, 5], self.option_repo.list(2))

  def test_get_options_for_invalid_part(self):
    self.assertEqual([], self.option_repo.list(6))

  def test_get_invalid_option(self):
    self.assertIsNone(self.option_repo.get(14))
  
  def test_get_incompatibilities_for_option(self):
    self.assertEqual([7], self.option_repo.list_incompatibilies(2))
    self.assertEqual([7], self.option_repo.list_incompatibilies(3))
    self.assertEqual([9], self.option_repo.list_incompatibilies(8))

  def test_get_incompatibilities_for_invalid_option(self):
    self.assertEqual([], self.option_repo.list_incompatibilies(1))

  def test_get_price_modifiers(self):
    depending_options = self.option_repo.list_depending_options(2)
    self.assertEqual([2], depending_options)

    price_coefs = [self.option_repo.get_depending_option_price_coef(2, id)
                   for id in depending_options]
    self.assertEqual([0.7], price_coefs)
  
  def test_get_price_modifiers_for_invalid_option(self):
    self.assertEqual([], self.option_repo.list_depending_options(1))
    self.assertEqual(1, self.option_repo.get_depending_option_price_coef(1, 2))
