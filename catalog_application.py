from abc import ABC, abstractmethod
import os
from typing import Iterable

import requests
from sqlalchemy import create_engine

from catalog.application import CalculatePriceCommand, GetPartOptionsCommand, \
  GetProductPartsCommand, GetProductsCommand
from catalog.domain import PartOption, Product, ProductId, ProductPart, \
  ProductPartId
from catalog.sqlalchemy_infra import create_models, \
  SqlAlchemyPartOptionRepository, SqlAlchemyProductPartRepository, \
  SqlAlchemyProductRepository
from test.integration.init_part_option_repository \
  import init_part_option_repository
from test.integration.init_product_part_repository \
  import init_product_part_repository
from test.integration.init_product_reposity import init_product_repository

class CatalogApplication(ABC):
  @abstractmethod
  def calculate_price(self, selected: Iterable[PartOption]) -> float:
    pass

  @abstractmethod
  def get_part_options(
      self,
      part_id: ProductPartId,
      selected: Iterable[PartOption]) -> Iterable[PartOption]:
    pass

  @abstractmethod
  def get_product_parts(self, product_id: ProductId) -> Iterable[ProductPart]:
    pass

  @abstractmethod
  def get_products(self) -> Iterable[Product]:
    pass


class LocalCatalogApplication(CatalogApplication):
  def __init__(self):
    engine = create_engine('sqlite+pysqlite:///:memory:')
    create_models(engine)
    self._product_repo = SqlAlchemyProductRepository(engine)
    self._part_repo = SqlAlchemyProductPartRepository(engine)
    self._option_repo = SqlAlchemyPartOptionRepository(engine)
    init_product_repository(self._product_repo)
    init_product_part_repository(self._part_repo)
    init_part_option_repository(self._option_repo)
    self._get_products = GetProductsCommand(self._product_repo)
    self._get_parts = GetProductPartsCommand(self._part_repo)
    self._get_options = GetPartOptionsCommand(self._option_repo)
    self._calculate_price = CalculatePriceCommand(self._option_repo)

  def calculate_price(self, selected: Iterable[PartOption]) -> float:
    return self._calculate_price(selected)

  def get_part_options(
      self,
      part_id: ProductPartId,
      selected: Iterable[PartOption]) -> Iterable[PartOption]:
    return self._get_options(part_id, selected)

  def get_product_parts(self, product_id: ProductId) -> Iterable[ProductPart]:
    return self._get_parts(product_id)

  def get_products(self) -> Iterable[Product]:
    return self._get_products()


class RemoteCatalogApplication(CatalogApplication):
  def __init__(self, url: str) -> None:
    self._base_url = url

  def calculate_price(self, selected: Iterable[PartOption]) -> float:
    result = requests.get(os.path.join(self._base_url, 'price'), params={
      'selected_options': self._join_options(selected),
    })
    result.raise_for_status()
    return float(result.json()['price'])
  
  @staticmethod
  def _join_options(options: Iterable[PartOption]) -> str:
    return ','.join([str(opt.id) for opt in options])

  def get_part_options(
      self,
      part_id: ProductPartId,
      selected: Iterable[PartOption]) -> Iterable[PartOption]:
    result = requests.get(os.path.join(self._base_url, 'part_options'), params={
      'product_part': part_id,
      'selected_options': self._join_options(selected),
    })
    result.raise_for_status()
    return [PartOption(**opt) for opt in result.json()]

  def get_product_parts(self, product_id: ProductId) -> Iterable[ProductPart]:
    result = requests.get(os.path.join(self._base_url, 'product_parts'), params={
      'product': product_id,
    })
    result.raise_for_status()
    return [ProductPart(**part) for part in result.json()]

  def get_products(self) -> Iterable[Product]:
    result = requests.get(os.path.join(self._base_url, 'products'))
    result.raise_for_status()
    return [Product(**product) for product in result.json()]


def create_catalog_app(url: str = None) -> CatalogApplication:
  return RemoteCatalogApplication(url) if url else LocalCatalogApplication()
