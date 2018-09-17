from player.player import Player
from leaderboard.leaderboard import Leaderboard
from players_table.playersTable import PlayersTable

class FileHandler:
    
#
# READ FILE METHODS
#

    def readPlayers(self):
        playerNames = self.readFile("player/storedPlayers.txt")
        players = []
        for name in playerNames:
            player = Player(name)
            players.append(player)
        playersTable = PlayersTable(players)
        return playersTable

    def readLeaderboard(self, leaderboardName):
        playerNames = self.readFile("leaderboard/" + leaderboardName + ".txt")
        players = []
        for name in playerNames:
            player = Player(name)
            players.append(player)
        leaderboard = Leaderboard(leaderboardName, players)
        return leaderboard

    def readLeaderboardNames(self):
        leaderboardNames = self.readFile("leaderboard/leaderboardNames.txt")
        return leaderboardNames

    def readFile(self, filename):
        myFile = open(filename, "r")
        contents = myFile.read().splitlines()
        myFile.close()
        return contents