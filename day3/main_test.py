import unittest
from devtools import debug

from main import find_max_joltage

class Tests(unittest.TestCase):
    def test_find_largest_twelve_digits(self):
        result = find_max_joltage("987654321111111", 12)
        debug(result)
        assert result == "987654321111"

if __name__ == "__main__":
    unittest.main()