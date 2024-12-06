from catalog.domain import Description
from catalog.sqlalchemy_infra import SqlAlchemyPartOptionRepository


def init_part_option_repository(repo: SqlAlchemyPartOptionRepository) -> None:
    options = [
        (1, Description('Full-suspension'), 130, True),
        (1, Description('Diamond'), 100, True),
        (1, Description('Step-through'), 90, True),
        (2, Description('Matte'), 50, True),
        (2, Description('Shiny'), 30, True),
        (3, Description('Road wheels'), 80, True),
        (3, Description('Mountain wheels'), 90, True),
        (3, Description('Fat bike wheels'), 100, True),
        (4, Description('Red'), 20, True),
        (4, Description('Black'), 25, True),
        (4, Description('Blue'), 20, True),
        (5, Description('Single-speed chain'), 43, True),
        (5, Description('8-speed chain'), 90, False),
    ]
    incompatibilities = [
        (2, 7),
        (3, 7),
        (8, 9),
    ]
    price_modifiers = [
        (2, 2, 0.7)
    ]
    for opt in options:
        repo.create(*opt)
    for incomp in incompatibilities:
        repo.create_incompatibility(*incomp)
    for modif in price_modifiers:
        repo.create_depending_option(*modif)
    repo.commit()
