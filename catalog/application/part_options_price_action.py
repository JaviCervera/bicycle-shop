from functools import reduce
from math import prod
from typing import Iterable

from catalog.domain import Money, PartOption, PartOptionId, \
    PartOptionRepository
from .log import log


class PartOptionsPriceAction:
    def __init__(self, repo: PartOptionRepository):
        self._repo = repo

    @log
    def __call__(self, selected: Iterable[PartOption]) -> Money:
        option_ids = [opt.id for opt in selected]
        return reduce(
            lambda money, opt: money + self._calc_price(opt, option_ids),
            selected,
            Money(0))

    @log
    def _calc_price(
            self, option: PartOption, used_option_ids: Iterable[PartOptionId]) -> Money:
        depending_opts = self._repo.list_depending_options(option.part_id)
        coefs = [self._repo.get_depending_option_price_coef(option.part_id, opt)
                 for opt in depending_opts if opt in used_option_ids]
        return option.price * prod(coefs)
