import unittest
from leaderboard import Leaderboard
from player.player import Player

class TestLeaderboard(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("John")
        self.player2 = Player("Mike")
        self.player3 = Player("Malik")

        self.players_list = [self.player1, self.player2]
        self.leaderboard = Leaderboard("Leaderboard", self.players_list)

        self.empty_leaderboard = Leaderboard("Leaderboard", [])

    #
    # in_rankings tests
    #
    def test_player_in_rankings_true(self):
        self.assertTrue(self.leaderboard.playerInRankings(self.player1))

    def test_player_in_rankings_false_populated(self):
        self.assertFalse(self.leaderboard.playerInRankings(self.player3))

    def test_player_in_rankings_false_empty(self):
        self.assertFalse(self.empty_leaderboard.playerInRankings(self.player1))

    #
    # remove_player tests
    #

    def test_remove_player_success(self):
        result = self.leaderboard.removePlayer(self.player1)
        new_rankings = self.leaderboard.getRankings()
        self.assertTrue(result)
        self.assertListEqual(new_rankings, [self.player2])

    def test_remove_player_fail_populated(self):
        result = self.leaderboard.removePlayer(self.player3)
        new_rankings = self.leaderboard.getRankings()
        self.assertFalse(result)
        self.assertListEqual(new_rankings, [self.player1, self.player2])

    def test_remove_player_fail_empty(self):
        result = self.empty_leaderboard.removePlayer(self.player1)
        new_rankings = self.empty_leaderboard.getRankings()
        self.assertFalse(result)
        self.assertListEqual(new_rankings, [])


    #
    # player tests
    #

    def test_get_player_position(self):
        position = self.leaderboard.getPlayerPosition("John")

        self.assertTrue(position, 1)


if __name__ == "__main__":
    unittest.main()