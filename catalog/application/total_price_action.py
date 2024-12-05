from logging import Logger
from math import prod
from typing import Iterable

from catalog.domain import PartOption, PartOptionId, PartOptionRepository
from catalog.domain.validations import validate_iterable, validate_type


class TotalPriceAction:
    def __init__(self, repo: PartOptionRepository, logger: Logger):
        validate_type(repo, PartOptionRepository, 'repo')
        validate_type(logger, Logger, 'logger')
        self._repo = repo
        self._logger = logger

    def __call__(self, selected: Iterable[PartOption]) -> float:
        validate_iterable(selected, PartOption, 'selected')
        self._logger.info(f'TotalPriceAction({selected}) called')
        option_ids = [opt.id for opt in selected]
        total = sum([self._calc_price(opt, option_ids) for opt in selected])
        self._logger.info(f'TotalPriceAction({selected} result: {total})')
        return total

    def _calc_price(
            self, option: PartOption, used_option_ids: Iterable[PartOptionId]) -> float:
        depending_opts = self._repo.list_depending_options(option.part_id)
        coefs = [self._repo.get_depending_option_price_coef(option.part_id, opt)
                 for opt in depending_opts if opt in used_option_ids]
        return option.price * prod(coefs)
