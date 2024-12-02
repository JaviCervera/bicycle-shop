from catalog.domain import PartOptionRepository

def init_part_option_repository(repo: PartOptionRepository) -> None:
  options = [
    (1, 'Full-suspension', 130, True),
    (1, 'Diamond', 100, True),
    (1, 'Step-through', 90, True),
    (2, 'Matte', 50, True),
    (2, 'Shiny', 30, True),
    (3, 'Road wheels', 80, True),
    (3, 'Mountain wheels', 90, True),
    (3, 'Fat bike wheels', 100, True),
    (4, 'Red', 20, True),
    (4, 'Black', 25, True),
    (4, 'Blue', 20, True),
    (5, 'Single-speed chain', 43, True),
    (5, '8-speed chain', 90, False),
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
