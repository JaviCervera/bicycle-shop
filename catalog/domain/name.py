from dataclasses import dataclass


@dataclass(frozen=True)
class Name:
    name: str

    def __post_init__(self):
        if not self.name:
            raise ValueError('Name must be a non empty string')

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name

    def __str__(self) -> str:
        return self.name
