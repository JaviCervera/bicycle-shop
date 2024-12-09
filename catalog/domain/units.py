from dataclasses import dataclass

@dataclass(frozen=True)
class Units:
  """
  The number of available units for a part option.
  The value cannot be negative.
  """
  units: int

  def __post_init__(self):
    if self.units < 0:
      raise ValueError('Units must not be negative')
  
  def __add__(self, other: 'Units') -> 'Units':
    return Units(self.units + other.units)
  
  def __sub__(self, other: 'Units') -> 'Units':
    return Units(self.units - other.units)
  
  def __int__(self) -> int:
    return int(self.units)
  
  def __str__(self) -> str:
    return str(self.units)
