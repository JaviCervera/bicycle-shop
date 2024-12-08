from unittest import TestCase

from catalog.domain import Name


class TestName(TestCase):
    def test_names_are_equal_if_have_same_name_and_class(self):
        self.assertEqual(Name('Bicycle'), Name('Bicycle'))
    
    def test_names_are_not_equal_if_dont_match(self):
        self.assertNotEqual(Name('Bicycle'), Name('Ball'))
    
    def test_name_is_not_equal_to_str(self):
        self.assertNotEqual('Bicycle', Name('Bicycle'))
    
    def test_name_can_be_converted_to_str(self):
        self.assertEqual('Bicycle', str(Name('Bicycle')))
    
    def test_name_cannot_be_empty(self):
        with self.assertRaises(ValueError) as context:
            Name('')
        self.assertEqual('Name must be a non empty string', str(context.exception))
