from math import prod
from typing import Iterable

from catalog.domain import PartOption, PartOptionId, PartOptionRepository
from catalog.domain.validations import validate_iterable, validate_type


class CalculatePriceCommand:
    def __init__(self, repo: PartOptionRepository):
        validate_type(repo, PartOptionRepository, 'repo')
        self._repo = repo

    def __call__(self, selected: Iterable[PartOption]) -> float:
        validate_iterable(selected, PartOption, 'selected')
        option_ids = [opt.id for opt in selected]
        return sum([self._calc_price(opt, option_ids) for opt in selected])

    def _calc_price(
            self, option: PartOption, used_option_ids: Iterable[PartOptionId]) -> float:
        depending_opts = self._repo.list_depending_options(option.part_id)
        coefs = [self._repo.get_depending_option_price_coef(option.part_id, opt)
                 for opt in depending_opts if opt in used_option_ids]
        return option.price * prod(coefs)
