from unittest import TestCase

from catalog.application import ProductsAction
from catalog.domain import Name, Product, ProductId
from .mock_product_repository import MockProductRepository


class TestProductsAction(TestCase):
    def test_returns_products_for_all_ids_in_repo(self):
        products = ProductsAction(MockProductRepository())
        self.assertEqual(
            [Product(ProductId(1), Name('Bicycles'))],
            products()
        )
