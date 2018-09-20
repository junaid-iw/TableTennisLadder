from player.player import Player
from players_table.playersTable import PlayersTable
from leaderboard.leaderboard import Leaderboard

class Reader:
    def readPlayers(self):
        playerNames = self.readFile("../player/storedPlayers.txt")
        players = []

        for name in playerNames:
            player = Player(name)
            players.append(player)

        return PlayersTable(players)

    def readLeaderboard(self, leaderboardName):
        playerNames = self.readFile("../leaderboard/" + leaderboardName + ".txt")
        players = []
        for name in playerNames:
            player = Player(name)
            players.append(player)
        leaderboard = Leaderboard(leaderboardName, players)

        return leaderboard

    def readLeaderboardNames(self):
        leaderboardNames = self.readFile("../leaderboard/leaderboardNames.txt")

        return leaderboardNames

    def readFile(self, filename):
        myFile = open(filename, "r")
        contents = myFile.read().splitlines()
        myFile.close()

        return contents