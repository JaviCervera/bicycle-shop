from unittest import TestCase

from catalog.domain import Money


class TestMoney(TestCase):
    def test_money_can_be_added(self):
        self.assertEqual(Money(11), Money(1) + Money(10))
    
    def test_money_can_be_multiplied_by_coefficient(self):
        self.assertEqual(Money(12.5), Money(10) * 1.25)
    
    def test_money_can_be_converted_to_float(self):
        self.assertEqual(20, float(Money(20)))
    
    def test_money_can_be_converted_to_str(self):
        self.assertEqual('1', str(Money(1)))
    
    def test_money_cannot_be_negative(self):
        with self.assertRaises(ValueError) as context:
            Money(-1)
        self.assertEqual('Money must not be negative', str(context.exception))
