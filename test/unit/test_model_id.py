from unittest import TestCase

from catalog.domain.model_id import ModelId


class TestModelId(TestCase):
    def test_converting_to_int_gives_wrapped_id(self):
        self.assertEqual(100, int(ModelId(100)))
  
    def test_converting_to_str_gives_string_formatted_id(self):
        self.assertEqual('25', str(ModelId(25)))
    
    def test_two_ids_are_equal_if_class_and_wrapped_id_are_equal(self):
        self.assertEqual(ModelId(1), ModelId(1))
    
    def test_two_ids_are_not_equal_if_wrapped_id_is_different(self):
        self.assertNotEqual(ModelId(1), ModelId(2))
    
    def test_two_ids_are_not_equal_if_class_is_different(self):
        class SubTypeId(ModelId):
            pass
        self.assertNotEqual(SubTypeId(1), ModelId(1))

    def test_ids_cannot_be_zero(self):
        with self.assertRaises(ValueError) as context:
            ModelId(0)
        self.assertEqual(
            'Id must be a positive integer',
            str(context.exception))
    
    def test_ids_cannot_be_negative(self):
        with self.assertRaises(ValueError) as context:
            ModelId(-1)
        self.assertEqual(
            'Id must be a positive integer',
            str(context.exception))
