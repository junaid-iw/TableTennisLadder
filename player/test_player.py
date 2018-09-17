import unittest
from player import Player

class TestPlayer(unittest.TestCase):
    def test_eq(self):
        player1 = Player("John")
        player2 = Player("John")

        self.assertTrue(player1 == player2)

    def test_ne(self):
        player1 = Player("John")
        player2 = Player("Mike")

        self.assertFalse(player1 == player2)

if __name__ == "__main__":
    unittest.main()