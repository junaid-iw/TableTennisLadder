class PlayersTable:
    def __init__(self, players):
        self.players = players

    # def getName(self):
    #    return self.name
    
    def getPlayers(self):
        return self.players
    
    # def setName(self, newName):
    #    self.name = newName
    
    def setPlayers(self, newplayers):
        self.players = newplayers

    def playerInTable(self, player):
        if player in self.players:
            return True
        else:
            return False
            
    def addPlayer(self, player):
        self.players.append(player)

    def removePlayer(self, player):
        self.players.remove(player)

    

    