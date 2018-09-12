class Leaderboard:
    def __init__(self, name, rankings):
        self.rankings = rankings

    def getName(self):
        return self.name
    
    def getRankings(self):
        return self.rankings

    def setRankings(self, newRankings):
        self.rankings = newRankings
    
    def setName(self, newName):
        self.name = newName
    
    def playerInRankings(self, player):
        if player in self.rankings:
            return True
        else:
            return False

    def addPlayer(self, player):
        self.rankings.append(player)

    def removePlayer(self, player):
        self.rankings.remove(player)

    def getPlayerPosition(self, player):
        return self.rankings.index(player)
    
    def updateAfterMatch(self, winner, loser):
        if not self.playerInRankings(winner):
            self.addPlayer(winner)
    
        if not self.playerInRankings(loser):
            self.addPlayer(loser)

        winnerPosition = self.getPlayerPosition(winner)
        loserPosition = self.getPlayerPosition(loser)
        if winnerPosition > loserPosition:
            oldRankings = self.rankings
            self.rankings = oldRankings[:loserPosition] + [winner] + oldRankings[loserPosition:winnerPosition] + oldRankings[winnerPosition + 1:]


    