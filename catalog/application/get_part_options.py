from itertools import chain
from typing import Iterable

from catalog.domain import PartOption, PartOptionRepository, ProductPartId
from catalog.domain.validations import validate_iterable, validate_type


class GetPartOptionsCommand:
    def __init__(self, repo: PartOptionRepository):
        validate_type(repo, PartOptionRepository, 'repo')
        self._repo = repo

    def __call__(
            self,
            part_id: ProductPartId,
            selected: Iterable[PartOption]) -> Iterable[PartOption]:
        validate_type(part_id, ProductPartId, 'part_id')
        validate_iterable(selected, PartOption, 'selected')
        return self._in_stock(self._compatible(part_id, selected))

    def _compatible(
            self,
            part_id: ProductPartId,
            selected_options: Iterable[PartOption]) -> Iterable[PartOption]:
        return [self._repo.get(opt)
                for opt in self._repo.list(part_id)
                if opt not in self._all_incompatibilities(selected_options)]

    def _all_incompatibilities(
            self, selected_options: Iterable[PartOption]) -> Iterable[int]:
        return set(chain.from_iterable(
            [self._repo.list_incompatibilities(opt.id)
             for opt in selected_options]))

    @staticmethod
    def _in_stock(options: Iterable[PartOption]) -> Iterable[PartOption]:
        return [opt for opt in options if opt.in_stock]
