from itertools import chain
from logging import Logger
from typing import Iterable

from catalog.domain import PartOption, PartOptionId, PartOptionRepository, \
    ProductPartId
from catalog.domain.validations import validate_iterable, validate_type


class PartOptionsAction:
    def __init__(self, repo: PartOptionRepository, logger: Logger):
        validate_type(repo, PartOptionRepository, 'repo')
        validate_type(logger, Logger, 'logger')
        self._repo = repo
        self._logger = logger

    def __call__(
            self,
            part_id: ProductPartId,
            selected: Iterable[PartOption]) -> Iterable[PartOption]:
        self._logger.info(f'PartOptionsAction({part_id}, {selected}) called')
        validate_type(part_id, ProductPartId, 'part_id')
        validate_iterable(selected, PartOption, 'selected')
        options = self._in_stock(self._compatible(part_id, selected))
        self._logger.info(f'PartOptionsAction({part_id}, {selected}) result: '
                          f'{options}')
        return options

    def _compatible(
            self,
            part_id: ProductPartId,
            selected_options: Iterable[PartOption]) -> Iterable[PartOption]:
        part_options = self._repo.list(part_id)
        self._logger.debug(f'PartOptionsAction._compatible has found the '
                           f'following options for part {part_id}:'
                           f' {part_options}')
        all_incompatibilities = self._all_incompatibilities(selected_options)
        return [self._repo.get(opt)  # type: ignore
                for opt in part_options
                if opt not in all_incompatibilities]

    def _all_incompatibilities(
            self, selected_options: Iterable[PartOption]) -> Iterable[PartOptionId]:
        incomps = [self._repo.list_incompatibilities(opt.id)
                   for opt in selected_options]
        flattened_set = set(chain.from_iterable(incomps))
        self._logger.debug(f'PartOptionsAction._all_incompatibilities'
                           f'({selected_options}): {flattened_set}')
        return flattened_set

    def _in_stock(self, options: Iterable[PartOption]) -> Iterable[PartOption]:
        in_stock = [opt for opt in options if opt.in_stock]
        self._logger.debug(f'PartOptionsAction._in_stock({options}): {in_stock}')
        return in_stock
