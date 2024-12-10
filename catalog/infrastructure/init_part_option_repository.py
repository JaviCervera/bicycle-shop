from catalog.domain import Money, Name, PartOptionId, ProductPartId, Units
from catalog.infrastructure import SqlAlchemyPartOptionRepository


def init_part_option_repository(repo: SqlAlchemyPartOptionRepository) -> None:
    """
    Utility function that initialized a SqlAlchemyPartOptionRepository with
    test data.
    """
    options = [
        (ProductPartId(1), Name('Full-suspension'), Money(130), Units(10)),
        (ProductPartId(1), Name('Diamond'), Money(100), Units(7)),
        (ProductPartId(1), Name('Step-through'), Money(90), Units(3)),
        (ProductPartId(2), Name('Matte'), Money(50), Units(5)),
        (ProductPartId(2), Name('Shiny'), Money(30), Units(7)),
        (ProductPartId(3), Name('Road wheels'), Money(80), Units(24)),
        (ProductPartId(3), Name('Mountain wheels'), Money(90), Units(1)),
        (ProductPartId(3), Name('Fat bike wheels'), Money(100), Units(15)),
        (ProductPartId(4), Name('Red'), Money(20), Units(20)),
        (ProductPartId(4), Name('Black'), Money(25), Units(32)),
        (ProductPartId(4), Name('Blue'), Money(20), Units(11)),
        (ProductPartId(5), Name('Single-speed chain'), Money(43), Units(6)),
        (ProductPartId(5), Name('8-speed chain'), Money(90), Units(0)),
    ]
    incompatibilities = [
        (PartOptionId(2), PartOptionId(7)),
        (PartOptionId(3), PartOptionId(7)),
        (PartOptionId(8), PartOptionId(9)),
    ]
    price_modifiers = [
        (ProductPartId(2), PartOptionId(2), 0.7)
    ]
    for opt in options:
        repo.create(*opt)
    for incomp in incompatibilities:
        repo.create_incompatibility(*incomp)
    for modif in price_modifiers:
        repo.create_depending_option(*modif)
