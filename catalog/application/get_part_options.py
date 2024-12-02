from itertools import chain
from typing import Iterable

from catalog.domain import PartOption, PartOptionRepository, ProductPart
from catalog.domain.validations import validate_iterable, validate_type

class GetPartOptionsCommand:
  def __init__(self, repo: PartOptionRepository):
    validate_type(repo, PartOptionRepository, 'repo')
    self._repo = repo

  def __call__(
      self,
      part: ProductPart,
      selected: Iterable[PartOption]) -> Iterable[PartOption]:
    validate_type(part, ProductPart, 'part')
    validate_iterable(selected, 'selected')
    return self._in_stock(self._compatible(part, selected))

  def _compatible(
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

  def _in_stock(
      self, options: Iterable[PartOption]) -> Iterable[PartOption]:
    return [opt for opt in options if opt.in_stock]
