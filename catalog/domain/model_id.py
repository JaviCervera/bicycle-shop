from dataclasses import dataclass


@dataclass(frozen=True)
class ModelId:
    """ Base class for the id type of all entities. """
    id: int

    def __post_init__(self):
        if self.id < 1:
            raise ValueError('Id must be a positive integer')

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id

    def __int__(self):
        return self.id

    def __str__(self) -> str:
        return str(self.id)
