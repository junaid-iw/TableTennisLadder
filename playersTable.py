class PlayersTable:
    def __init__(self, players):
        self.players = players
    
    def getPlayers(self):
        return self.players
    
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

    

    