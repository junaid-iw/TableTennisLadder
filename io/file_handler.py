from player.player import Player
from leaderboard.leaderboard import Leaderboard
from players_table.playersTable import PlayersTable
from file_read_write import FileReadWrite

# fileReadWrite = FileReadWrite("player/storedPlayers.txt")
# fileHandler = FileHandler(fileReadWrite)
# playersList = FileHandler.readPlayers

class FileHandler:
    
    def __init__(self, fileReadWrite):
        self.fileReadWrite = fileReadWrite

#
# READ FILE METHODS
#

    def getFileList(self):
        fileContents = self.fileReadWrite.readFile()
        fileList = fileContents.splitlines()
        return fileList

    def getPlayersFromFile(self):
        playerNames = self.fileReadWrite.readFile()
        players = []
        for name in playerNames:
            player = Player(name)
            players.append(player)
        return players

    def getPlayersTableFromFile(self):
        players = getPlayersFromFile()
        playersTable = PlayersTable(players)
    
    def getLeaderboardFromFile(self, leaderboardName):
        players = getPlayersFromFile()
        Leaderboard = Leaderboard(leaderboardName, players)

    def readPlayers(self):
        playerNames = self.fileReadWrite.readFile()
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

    #
    # WRITE FILE METHODS
    #

    def updateFile(self, listForFile):
        contents = ""
        for item in listForFile:
            contents.append(item + "\n")
        self.fileReadWrite.writeFile(contents)

    def updatePlayersTable(self, playersTable):
        players = playersTable.getPlayers()
        playerNames = []
        for player in players:
            playerNames.append(player.getName())
        updateFile("player/storedPlayers.txt", playerNames)

    def updateLeaderboard(self, leaderboard):
        players = leaderboard.getRankings()
        playerNames = []
        for player in players:
            playerNames.append(player.getName())
        leaderboardName = leaderboard.getName()
        updateFile("leaderboard/" + leaderboardName + ".txt", playerNames)

    def updateLeaderboardNames(self, leaderboardNames):
        updateFile("leaderboard/leaderboardNames.txt", leaderboardNames)

    # Reorders the leaderboardNames.txt file so the current leaderboard's name is first
    def reorderLeaderboardNames(self, newCurrentLeaderboardName, leaderboardNames):
        if newCurrentLeaderboardName in leaderboardNames:
            newCurrentLearderboardNamePosition = leaderboardNames.index(newCurrentLeaderboardName)
            reorderedLeaderboardNames = [newCurrentLeaderboardName] + leaderboardNames[:newCurrentLearderboardNamePosition] + leaderboardNames[newCurrentLearderboardNamePosition + 1:]
        else:
            reorderedLeaderboardNames = [newCurrentLeaderboardName] + leaderboardNames
        updateFile("leaderboard/leaderboardNames.txt", reorderedLeaderboardNames)