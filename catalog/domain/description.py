from dataclasses import dataclass


@dataclass(frozen=True)
class Description:
    desc: str

    def __post_init__(self):
        if not self.desc:
            raise ValueError('Description must be a non empty string')

    def __str__(self) -> str:
        return self.desc
