import unittest
from jsonxplode import FlattenJson


class FlattenTestCases(unittest.TestCase):
    def test_example_1(self):
        input_json = {
            "name": "John",
            "a": [1, 2, 3],
            "b": [1, 2, 3]
        }
        expected = [
            {"name": "John", "a": 1, "b": 1},
            {"name": "John", "a": 2, "b": 2},
            {"name": "John", "a": 3, "b": 3}
        ]
        flattener = FlattenJson()
        flattener.flatten_json(input_json)
        self.assertEqual(flattener.complete_data, expected)