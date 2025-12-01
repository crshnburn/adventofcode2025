import unittest

from main import turnDial, turnDial2

class TestTurnDial(unittest.TestCase):

    def test_turnDial(self):
        instructions = [
            'L68',
            'L30',
            'R48',
            'L5',
            'R60',
            'L55',
            'L1',
            'L99',
            'R14',
            'L82'
        ]
        assert turnDial(instructions) == 3
    
    def test_turnDial2(self):
        instructions = [
            'L68',
            'L30',
            'R48',
            'L5',
            'R60',
            'L55',
            'L1',
            'L99',
            'R14',
            'L82'
        ]
        # assert turnDial2(instructions) == 6
        assert turnDial2(['R1000']) == 10

# Run tests
if __name__ == '__main__':
    unittest.main()