from itertools import chain
from typing import Iterable

from catalog.domain import PartOption, ProductPart
from .part_option_repository import PartOptionRepository

class PartOptionFilter:
  def __init__(self, opt_repository: PartOptionRepository):
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
