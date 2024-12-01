from dataclasses import dataclass
from itertools import chain
from math import prod
from typing import Iterable


@dataclass(frozen=True)
class Product:
  id: int
  description: str


@dataclass(frozen=True)
class ProductPart:
  id: int
  product_id: int
  description: str


@dataclass(frozen=True)
class PartOption:
  id: int
  part_id: int
  description: str
  price: float
  in_stock: bool


class PartOptionFilter:
  def __init__(self, opt_repository: 'PartOptionRepository'):
    self._repo = opt_repository

  def compatible(
      self,
      product_part: ProductPart,
      selected_options: Iterable[PartOption]) -> Iterable[PartOption]:
    return [self._repo.get(opt)
            for opt in self._repo.list(product_part.id)
            if opt not in self._all_incompatibilities(selected_options)]
  
  def _all_incompatibilities(
      self, selected_options: Iterable[PartOption]) -> Iterable[int]:
    return chain.from_iterable(
      [self._repo.list_incompatibilies(opt.id)
       for opt in selected_options])

  def in_stock(
      self, options: Iterable[PartOption]) -> Iterable[PartOption]:
    return [opt for opt in options if opt.in_stock]


class PriceCalculator:
  def __init__(self, opt_repository: 'PartOptionRepository'):
    self._repo = opt_repository

  def __call__(self, options: Iterable[PartOption]) -> float:
    option_ids = [opt.id for opt in options]
    return sum([self._calc_price(opt, option_ids) for opt in options])

  def _calc_price(
      self, option: PartOption, used_option_ids: Iterable[int]) -> float:
    depending_opts = self._repo.list_depending_options(option.part_id)
    coefs = [self._repo.get_depending_option_price_coef(option.part_id, opt)
             for opt in depending_opts if opt in used_option_ids]
    return option.price * prod(coefs)
