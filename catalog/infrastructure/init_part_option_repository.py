from catalog.domain import Description, PartOptionId, ProductPartId
from catalog.infrastructure import SqlAlchemyPartOptionRepository


def init_part_option_repository(repo: SqlAlchemyPartOptionRepository) -> None:
    options = [
        (ProductPartId(1), Description('Full-suspension'), 130, True),
        (ProductPartId(1), Description('Diamond'), 100, True),
        (ProductPartId(1), Description('Step-through'), 90, True),
        (ProductPartId(2), Description('Matte'), 50, True),
        (ProductPartId(2), Description('Shiny'), 30, True),
        (ProductPartId(3), Description('Road wheels'), 80, True),
        (ProductPartId(3), Description('Mountain wheels'), 90, True),
        (ProductPartId(3), Description('Fat bike wheels'), 100, True),
        (ProductPartId(4), Description('Red'), 20, True),
        (ProductPartId(4), Description('Black'), 25, True),
        (ProductPartId(4), Description('Blue'), 20, True),
        (ProductPartId(5), Description('Single-speed chain'), 43, True),
        (ProductPartId(5), Description('8-speed chain'), 90, False),
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
    repo.commit()
