from typing import Optional, Sequence

from catalog.domain import PartOption


class PartOptionRepository:
  _options = [
    PartOption(1, 1, 'Full-suspension', 130),
    PartOption(2, 1, 'Diamond', 100),
    PartOption(3, 1, 'Step-through', 90),
    PartOption(4, 2, 'Matte', 50),
    PartOption(5, 2, 'Shiny', 30),
    PartOption(6, 3, 'Road wheels', 80),
    PartOption(7, 3, 'Mountain wheels', 90),
    PartOption(8, 3, 'Fat bike wheels', 100),
    PartOption(9, 14, 'Red', 20),
    PartOption(10, 4, 'Black', 25),
    PartOption(11, 4, 'Blue', 20),
    PartOption(12, 5, 'Single-speed chain', 43),
    PartOption(13, 5, '8-speed chain', 90),
  ]

  def list(self, part_id: int = None) -> Sequence[int]:
    if part_id is None:
      return [opt.id for opt in self._options]
    else:
      return [opt.id for opt in self._options if opt.part_id == part_id]

  def get(self, id: int) -> Optional[PartOption]:
    if id in range(1, 14):
      return self._options[id - 1]
    else:
      return None

  def list_incompatibilies(self, id: int) -> Sequence[int]:
    incompatibilities = {
      2: [7],
      3: [7],
      8: [9],
    }
    return incompatibilities.get(id, [])

  def list_dependents(self, id: int) -> Sequence[int]:
    dependents = {
      2: [4]
    }
    return dependents.get(id, [])

  def get_price_coef(self, id: int, dependent_id: int) -> float:
    coefs = {
      (2, 4): 0.7
    }
    return coefs.get((id, dependent_id), 1)
