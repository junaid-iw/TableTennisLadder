class Leaderboard:
    def __init__(self, rankings):
        self.rankings = rankings

    # def getName(self):
    #     return self.name
    
    def getRankings(self):
        return self.rankings
    
    # def setName(self, newName):
    #     self.name = newName
    
    def setRankings(self, newRankings):
        self.rankings = newRankings