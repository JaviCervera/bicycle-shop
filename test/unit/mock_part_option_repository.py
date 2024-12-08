from typing import Iterable, Optional

from catalog.domain import Money, Name, PartOption, PartOptionId, \
    PartOptionRepository, ProductPartId, Units


class MockPartOptionRepository(PartOptionRepository):
    _options = [
        PartOption(
            PartOptionId(1),
            ProductPartId(1),
            Name('Full-suspension'),
            Money(130),
            Units(10)),
        PartOption(
            PartOptionId(2),
            ProductPartId(1),
            Name('Diamond'),
            Money(100),
            Units(7)),
        PartOption(
            PartOptionId(3),
            ProductPartId(1),
            Name('Step-through'),
            Money(90),
            Units(3)),
        PartOption(
            PartOptionId(4),
            ProductPartId(2),
            Name('Matte'),
            Money(50),
            Units(5)),
        PartOption(
            PartOptionId(5),
            ProductPartId(2),
            Name('Shiny'),
            Money(30),
            Units(7)),
        PartOption(
            PartOptionId(6),
            ProductPartId(3),
            Name('Road wheels'),
            Money(80),
            Units(24)),
        PartOption(
            PartOptionId(7),
            ProductPartId(3),
            Name('Mountain wheels'),
            Money(90),
            Units(1)),
        PartOption(
            PartOptionId(8),
            ProductPartId(3),
            Name('Fat bike wheels'),
            Money(100),
            Units(15)),
        PartOption(
            PartOptionId(9),
            ProductPartId(4),
            Name('Red'),
            Money(20),
            Units(20)),
        PartOption(
            PartOptionId(10),
            ProductPartId(4),
            Name('Black'),
            Money(25),
            Units(32)),
        PartOption(
            PartOptionId(11),
            ProductPartId(4),
            Name('Blue'),
            Money(20),
            Units(11)),
        PartOption(
            PartOptionId(12),
            ProductPartId(5),
            Name('Single-speed chain'),
            Money(43),
            Units(6)),
        PartOption(
            PartOptionId(13),
            ProductPartId(5),
            Name('8-speed chain'),
            Money(90),
            Units(0)),
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
            name: Name,
            price: Money,
            available_units: Units) -> PartOption:
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
            coefficient: float) -> None:
        pass
