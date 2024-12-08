from dataclasses import dataclass


@dataclass(frozen=True)
class Description:
    desc: str

    def __post_init__(self):
        if not self.desc:
            raise ValueError('Description must be a non empty string')

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.desc == other.desc

    def __str__(self) -> str:
        return self.desc
