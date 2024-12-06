import logging
from itertools import chain
from typing import Iterable

from catalog.domain import PartOption, PartOptionId, PartOptionRepository, \
    ProductPartId
from .log import log


class PartOptionsAction:
    def __init__(self, repo: PartOptionRepository):
        self._repo = repo

    @log
    def __call__(
            self,
            part_id: ProductPartId,
            selected: Iterable[PartOption]) -> Iterable[PartOption]:
        options = self._in_stock(self._compatible(part_id, selected))
        return options

    @log
    def _compatible(
            self,
            part_id: ProductPartId,
            selected_options: Iterable[PartOption]) -> Iterable[PartOption]:
        part_options = self._repo.list(part_id)
        logging.debug(f'PartOptionsAction._compatible found the following '
                      f'options for part {part_id}: {part_options}')
        all_incompatibilities = self._all_incompatibilities(selected_options)
        return [self._repo.get(opt)  # type: ignore
                for opt in part_options
                if opt not in all_incompatibilities]

    @log
    def _all_incompatibilities(
            self, selected_options: Iterable[PartOption]) -> Iterable[PartOptionId]:
        incomps = [self._repo.list_incompatibilities(opt.id)
                   for opt in selected_options]
        return set(chain.from_iterable(incomps))

    @log
    def _in_stock(self, options: Iterable[PartOption]) -> Iterable[PartOption]:
        return [opt for opt in options if opt.in_stock]
