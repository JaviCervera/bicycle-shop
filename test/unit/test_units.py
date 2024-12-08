from unittest import TestCase

from catalog.domain import Units

class TestUnits(TestCase):
  def test_units_can_be_added(self):
    self.assertEqual(Units(10), Units(6) + Units(4))

  def test_units_can_be_subtracted(self):
    self.assertEqual(Units(2), Units(6) - Units(4))

  def test_units_can_be_converted_to_int(self):
    self.assertEqual(5, int(Units(5)))
  
  def test_units_can_be_converted_to_str(self):
    self.assertEqual('5', str(Units(5)))

  def test_units_cannot_be_negative(self):
    with self.assertRaises(ValueError) as context:
      Units(-1)
    self.assertEqual('Units must not be negative', str(context.exception))
