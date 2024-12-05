from typing import Iterable, Optional

from catalog.domain import PartOption, PartOptionId, PartOptionRepository, \
    ProductPartId


class MockPartOptionRepository(PartOptionRepository):
    _options = [
        PartOption(1, 1, 'Full-suspension', 130, True),
        PartOption(2, 1, 'Diamond', 100, True),
        PartOption(3, 1, 'Step-through', 90, True),
        PartOption(4, 2, 'Matte', 50, True),
        PartOption(5, 2, 'Shiny', 30, True),
        PartOption(6, 3, 'Road wheels', 80, True),
        PartOption(7, 3, 'Mountain wheels', 90, True),
        PartOption(8, 3, 'Fat bike wheels', 100, True),
        PartOption(9, 4, 'Red', 20, True),
        PartOption(10, 4, 'Black', 25, True),
        PartOption(11, 4, 'Blue', 20, True),
        PartOption(12, 5, 'Single-speed chain', 43, True),
        PartOption(13, 5, '8-speed chain', 90, False),
    ]

    def list(
            self,
            part_id: Optional[ProductPartId] = None) -> Iterable[PartOptionId]:
        if part_id is None:
            return [opt.id for opt in self._options]
        else:
            return [opt.id for opt in self._options if opt.part_id == part_id]

    def get(self, id_: PartOptionId) -> Optional[PartOption]:
        if id_ in range(1, 14):
            return self._options[id_ - 1]
        else:
            return None

    def create(
            self,
            part_id: ProductPartId,
            description: str,
            price: float,
            in_stock: bool) -> PartOption:
        raise NotImplementedError()

    def list_incompatibilities(
            self, id_: PartOptionId) -> Iterable[PartOptionId]:
        incompatibilities = {
            2: [7],
            3: [7],
            7: [2, 3],
            8: [9],
            9: [8],
        }
        return incompatibilities.get(id_, [])

    def create_incompatibility(
            self,
            option_id: PartOptionId,
            incompatible_option_id: PartOptionId) -> None:
        pass

    def list_depending_options(
            self, part_id: ProductPartId) -> Iterable[PartOptionId]:
        depending_opts = {
            2: [2]
        }
        return depending_opts.get(part_id, [])

    def get_depending_option_price_coef(
            self,
            part_id: ProductPartId,
            depending_option_id: PartOptionId) -> float:
        coefs = {
            (2, 2): 0.7
        }
        return coefs.get((part_id, depending_option_id), 1)

    def create_depending_option(
            self,
            part_id: ProductPartId,
            depending_option_id: PartOptionId,
            coef: float) -> None:
        pass
