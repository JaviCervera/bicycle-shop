from typing import Iterable, Optional

from catalog.domain import Description, PartOption, PartOptionId, \
    PartOptionRepository, ProductPartId


class MockPartOptionRepository(PartOptionRepository):
    _options = [
        PartOption(
            PartOptionId(1),
            ProductPartId(1),
            Description('Full-suspension'),
            130,
            True),
        PartOption(
            PartOptionId(2),
            ProductPartId(1),
            Description('Diamond'),
            100,
            True),
        PartOption(
            PartOptionId(3),
            ProductPartId(1),
            Description('Step-through'),
            90,
            True),
        PartOption(
            PartOptionId(4),
            ProductPartId(2),
            Description('Matte'),
            50,
            True),
        PartOption(
            PartOptionId(5),
            ProductPartId(2),
            Description('Shiny'),
            30,
            True),
        PartOption(
            PartOptionId(6),
            ProductPartId(3),
            Description('Road wheels'),
            80,
            True),
        PartOption(
            PartOptionId(7),
            ProductPartId(3),
            Description('Mountain wheels'),
            90,
            True),
        PartOption(
            PartOptionId(8),
            ProductPartId(3),
            Description('Fat bike wheels'),
            100,
            True),
        PartOption(
            PartOptionId(9),
            ProductPartId(4),
            Description('Red'),
            20,
            True),
        PartOption(
            PartOptionId(10),
            ProductPartId(4),
            Description('Black'),
            25,
            True),
        PartOption(
            PartOptionId(11),
            ProductPartId(4),
            Description('Blue'),
            20,
            True),
        PartOption(
            PartOptionId(12),
            ProductPartId(5),
            Description('Single-speed chain'),
            43,
            True),
        PartOption(
            PartOptionId(13),
            ProductPartId(5),
            Description('8-speed chain'),
            90,
            False),
    ]

    def list(
            self,
            part_id: Optional[ProductPartId] = None) -> Iterable[PartOptionId]:
        if part_id is None:
            return [opt.id for opt in self._options]
        else:
            return [opt.id for opt in self._options if opt.part_id == part_id]

    def get(self, id_: PartOptionId) -> Optional[PartOption]:
        if int(id_) in range(1, 14):
            return self._options[int(id_) - 1]
        else:
            return None

    def create(
            self,
            part_id: ProductPartId,
            description: Description,
            price: float,
            in_stock: bool) -> PartOption:
        raise NotImplementedError()

    def list_incompatibilities(
            self, id_: PartOptionId) -> Iterable[PartOptionId]:
        incompatibilities = {
            PartOptionId(2): [PartOptionId(7)],
            PartOptionId(3): [PartOptionId(7)],
            PartOptionId(7): [PartOptionId(2), PartOptionId(3)],
            PartOptionId(8): [PartOptionId(9)],
            PartOptionId(9): [PartOptionId(8)],
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
            ProductPartId(2): [PartOptionId(2)]
        }
        return depending_opts.get(part_id, [])

    def get_depending_option_price_coef(
            self,
            part_id: ProductPartId,
            depending_option_id: PartOptionId) -> float:
        coefs = {
            (ProductPartId(2), PartOptionId(2)): 0.7
        }
        return coefs.get((part_id, depending_option_id), 1)

    def create_depending_option(
            self,
            part_id: ProductPartId,
            depending_option_id: PartOptionId,
            coef: float) -> None:
        pass
