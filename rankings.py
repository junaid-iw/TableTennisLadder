import sys
from player import Player
from playersTable import PlayersTable
from leaderboard import Leaderboard


# Called when the user chooses to add a new player. Allows the user to add multiple players.
def addPlayersMenu(players):
    while (True):
        newPlayerName = requestName("Please enter the name of the new player: \n")
        newPlayer = Player(newPlayerName)

        addPlayerIfNew(players, newPlayer)
            
        if not askUserYNQuestion("Would you like to add another player?"):
            return players

# Removes players from both the players list and the leaderboard list
def removePlayersMenu(playersList, leaderboard):
    while (True):
        removedPlayerName = requestName("Please enter the name of the player you want to remove: \n")
        removedPlayer = Player(removedPlayerName)

        removePlayerIfInPlayersTable(playersList, leaderboard, removedPlayer)

        if not askUserYNQuestion("Would you ike to remove another player?"):
            return playersList, leaderboard

# Allows the user to input a winner and loser of a match, and updates the leaderboard table
# accordingly
def recordMatchMenu(players, leaderboard):
    winner = requestWinnerOrLoser("winner", players)
    loser = requestWinnerOrLoser("loser", players)
    leaderboard = updateLeaderboardAfterMatch(winner, loser, leaderboard)

    print("leaderboard updated!")
    return leaderboard

# Prints the leaderboard table to the screen
def seeLeaderboard(leaderboard):
    print("The current leaderboard are as follows: \n")

    players = leaderboard.getRankings()
    for position, player in enumerate(players, start=1):
        print str(position) + ". " + player.getName()
    print("")

# Quits the program
def quitProgram():
    print("Goodbye!")
    exit()






# Starts the interactive mode of the program
def clInteractive(players, leaderboard):
    players = readPlayers()
    leaderboard = readLeaderboard()

    print("Welcome to TZ Table Tennis (Copyright 2018. All rights reserved) \n")
    
    finished = False

    while (not finished):
        print("Please choose from one of the following options:")
        print("1) Add players")
        print("2) Remove players")
        print("3) Record match")
        print("4) See leaderboard")
        print("5) Exit \n")

        choice = raw_input()
        print("")

        if choice == "1":
            players = addPlayersMenu(players)
        elif choice == "2":
            players, leaderboard = removePlayersMenu(players, leaderboard)
        elif choice == "3":
            leaderboard = recordMatchMenu(players, leaderboard)
        elif choice == "4":
            seeLeaderboard(leaderboard)
        elif choice == "5":
            quitProgram()
        else:
            print("Invalid input. \n")

# Adds a new player (Unix interface)
def clAddPlayers(playersTable):
    if len(sys.argv) != 3:
        print("\n'-add' operator requires 1 parameter (name of player to be added)\n")
        sys.exit(1)
    
    playersTable = readPlayers()
    newPlayerName = sys.argv[2]
    newPlayer = Player(newPlayerName)

    addPlayerIfNew(playersTable, newPlayer)

# Removes a player (Unix interface)
def clRemovePlayers(players, leaderboard):
    if len(sys.argv) != 3:
        print("\n'-remove' operator requires 1 parameter (name of player to be removed)\n")
        sys.exit(1)
    
    playersTable = readPlayers()
    leaderboard = readLeaderboard()
    removedPlayerName = sys.argv[2]
    removedPlayer = Player(removedPlayerName)

    removePlayerIfInPlayersTable(playersTable, leaderboard, removedPlayer)
    return

# Records a match between two players, updating the leaderboard table (Unix interface)
def clRecordMatch(playersTable, leaderboard):
    if len(sys.argv) != 4:
        print("\n'-result' operator requires 2 parameters (name of winner, name of loser)\n")
        sys.exit(1)
    
    playersTable = readPlayers()
    leaderboard = readLeaderboard()

    winner = Player(sys.argv[2])
    loser = Player(sys.argv[3])

    if not playersTable.playerInTable(winner) and playersTable.playerInTable(loser):
        print("Neither player is part of this league")
    elif not playersTable.playerInTable(winner):
        print("The winner is not part of this league")
    elif not playersTable.playerInTable(loser):
        print("The loser is not part of this league")
    else:
        updateLeaderboardAfterMatch(winner, loser, leaderboard)
        print("Leaderboard updated!")



# Prints the current leaderboard to the terminal (Unix interface)
def clSeeleaderboard():
    if len(sys.argv) != 2:
        print("\n'-result' operator requires no parameters\n")
        sys.exit(1)
    
    leaderboard = readLeaderboard()
    seeLeaderboard(leaderboard)





# Adds a player to the players list, unless they are already in the players list
def addPlayerIfNew(playersTable, newPlayer):
    if playersTable.playerInTable(newPlayer):
            print("This player already in the players list.")
    else:
        addPlayer(playersTable, newPlayer)
        print("Player added!")

# Adds player to end of players list
def addPlayer(playersTable, newPlayer):
    playersTable.addPlayer(newPlayer)
    updatePlayersTable(playersTable)

# Removes a player from the players list (and leaderboard list if they're in that list),
# unless they are not in the players list
def removePlayerIfInPlayersTable(playersTable, leaderboard, removedPlayer):
    if not playersTable.playerInTable(removedPlayer):
            print("This player is not in the players list.")
    else:
        removePlayerFromPlayersTable(playersTable, removedPlayer)
        if leaderboard.playerInRankings(removedPlayer):
            removePlayerFromleaderboard(leaderboard, removedPlayer)
        print("Player removed!")

# Removes player from players list
def removePlayerFromPlayersTable(playersTable, playerToBeRemoved):
    playersTable.removePlayer(playerToBeRemoved)
    updatePlayersTable(playersTable)

# Removes player from leaderboard list
def removePlayerFromleaderboard(leaderboard, playerToBeRemoved):
    leaderboard.removePlayer(playerToBeRemoved)
    updateLeaderboard(leaderboard)

# Asks the user a yes/no question, returning false if anything
# but 'y' is entered
def askUserYNQuestion(question):
    print(question + " (y/n) \n")
    choice = raw_input()
    print("")
    if choice == "y":
        return True
    else:    # Stops the loop if anything but y entered
        return False

# Requests the name of a player from the user
def requestName(prompt):
    print(prompt)
    player = raw_input()
    print("")
    return player

# Requests a winner or a loser
def requestWinnerOrLoser(winnerOrLoser, players):
    while(True):
        player = requestName("Please enter the name of the match " + winnerOrLoser + ": \n")

        if (player not in players):
            print("This player is not in the league.")
        else:
            return player

# Updates the leaderboard list based on a winner and loser of a match
def updateLeaderboardAfterMatch(winner, loser, leaderboard):
    
    
    leaderboard.updateAfterMatch(winner, loser)

    updateLeaderboard(leaderboard)
    return leaderboard

def readPlayers():
    playerNames = readFile("storedPlayers.txt")
    players = []
    for name in playerNames:
        player = Player(name)
        players.append(player)
    playersTable = PlayersTable(players)
    return playersTable

def readLeaderboard():
    playerNames = readFile("storedLeaderboard.txt")
    players = []
    for name in playerNames:
        player = Player(name)
        players.append(player)
    leaderboard = Leaderboard(players)
    return leaderboard

def readFile(filename):
    myFile = open(filename, "r")
    contents = myFile.read().splitlines()
    myFile.close()
    return contents

def updatePlayersTable(playersTable):
    players = playersTable.getPlayers()
    updateFile("storedPlayers.txt", players)

def updateLeaderboard(leaderboard):
    players = leaderboard.getRankings()
    updateFile("storedLeaderboard.txt", players)

def updateFile(filename, players):
    myFile = open(filename, "w")
    for player in players:
        myFile.write(player.getName() + "\n")
    myFile.close()

# Main method
def main():
    
    players = []
    leaderboard = []
    
    if len(sys.argv) == 1:
        clSeeleaderboard()
        sys.exit(1)
    if sys.argv[1] == "--interactive":
        clInteractive(players, leaderboard)
    elif sys.argv[1] == "--add":
        clAddPlayers(players)
    elif sys.argv[1] == "--remove":
        clRemovePlayers(players, leaderboard)
    elif sys.argv[1] == "--result":
        clRecordMatch(players, leaderboard)
    elif sys.argv[1] == "--rank":
        clSeeleaderboard()
    else:
        print("Invalid input")

    
        
# def main():
#     if len(sys.argv) != 3:
#         print 'usage: ./leaderboard.py {winner | loser} file'
#         sys.exit(1)

#     leaderboard = ["matt", "junaid", "mike", "james", "sandeep"]
    
#     winner = sys.argv[1]
#     loser = sys.argv[2]

#     if winner in leaderboard and loser in leaderboard:
#         leaderboard = existingWin(leaderboard, winner, loser)
#     elif winner in leaderboard:
#         leaderboard = newLoser(leaderboard, loser)
#     elif loser in leaderboard:
#         leaderboard = newWinner(leaderboard, winner, loser)
#     else:
#         leaderboard = newPlayers(leaderboard, winner, loser)
#     #leaderboard = existingWin(leaderboard, "james", "matt")
#     #leaderboard = newLoser(leaderboard, "emily")
#     #leaderboard = newPlayers(leaderboard, "emily", "ash")
#     #leaderboard = newWinner(leaderboard, "emily", "junaid")

#     for player in leaderboard:
#         print(player)

if __name__ == '__main__':
  main()