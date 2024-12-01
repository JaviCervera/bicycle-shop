from math import prod
from typing import Iterable

from catalog.domain import PartOption
from .part_option_repository import PartOptionRepository


class PriceCalculator:
  def __init__(self, opt_repository: PartOptionRepository):
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
