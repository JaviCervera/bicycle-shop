from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    """ Money, which cannot be negative. """
    amount: float

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError('Money must not be negative')

    def __add__(self, other: 'Money') -> 'Money':
        return Money(self.amount + other.amount)

    def __mul__(self, coefficient: float) -> 'Money':
        return Money(self.amount * coefficient)

    def __float__(self) -> float:
        return float(self.amount)

    def __str__(self) -> str:
        return str(self.amount)
