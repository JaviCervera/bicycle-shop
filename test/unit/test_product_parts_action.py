from unittest import TestCase

from catalog.application import ProductPartsAction
from catalog.domain import Name, ProductId, ProductPart, ProductPartId
from .mock_product_part_repository import MockProductPartRepository


class TestProductPartsAction(TestCase):
  def test_only_returns_product_parts_for_requested_product(self):
    product_parts = ProductPartsAction(MockProductPartRepository())
    self.assertEqual(
        [
            ProductPart(
                ProductPartId(1), ProductId(1), Name('Frame type')),
            ProductPart(
                ProductPartId(2), ProductId(1), Name('Frame finish')),
            ProductPart(
                ProductPartId(3), ProductId(1), Name('Wheels')),
            ProductPart(
                ProductPartId(4), ProductId(1), Name('Rim color')),
            ProductPart(
                ProductPartId(5), ProductId(1), Name('Chain')),
        ],
        product_parts(ProductId(1)))
    self.assertEqual([], product_parts(ProductId(2)))
