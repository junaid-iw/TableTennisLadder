class Player:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name
    
    def setName(self, newName):
        self.name = newName

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.getName() == other.getName()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
