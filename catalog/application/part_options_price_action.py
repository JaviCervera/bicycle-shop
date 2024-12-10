from functools import reduce
from math import prod
from typing import Iterable

from catalog.domain import Money, PartOption, PartOptionId, \
    PartOptionRepository
from .log import log


class PartOptionsPriceAction:
    """
    Use case that lets the user calculate the price of the given part options,
    taking into account that some of the selected options can affect the price
    of others.
    """
    def __init__(self, repo: PartOptionRepository):
        self._repo = repo

    @log
    def __call__(self, selected: Iterable[PartOption]) -> Money:
        option_ids = [opt.id for opt in selected]
        return reduce(
            lambda money, option: money + self._calc_price(option, option_ids),
            selected,
            Money(0))

    @log
    def _calc_price(
            self,
            option: PartOption,
            selected_option_ids: Iterable[PartOptionId]) -> Money:
        """
        Calculate the price of one option, checking if any of the
        selected options modifies its price.
        """
        depending_opts = self._repo.list_depending_options(option.part_id)
        coefs = [self._repo.get_depending_option_price_coef(option.part_id, opt)
                 for opt in depending_opts if opt in selected_option_ids]
        return option.price * prod(coefs)
