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
            
        if askUserYNQuestion("Would you like to add another player?"):
            return players

# Removes players from both the players list and the leaderboard list
def removePlayersMenu(players, leaderboard):
    while (True):
        removedPlayerName = requestName("Please enter the name of the player you want to remove: \n")

        removePlayerIfExists(players, leaderboard, removedPlayer)

        if askUserYNQuestion("Would you ike to remove another player?"):
            return players, leaderboard

# Allows the user to input a winner and loser of a match, and updates the leaderboard table
# accordingly
def recordMatchMenu(players, leaderboard):
    winner = requestWinnerOrLoser("winner", players)
    loser = requestWinnerOrLoser("loser", players)
    leaderboard = updateLeaderboardAfterMatch(winner, loser, leaderboard)

    print("leaderboard updated!")
    return leaderboard

# Prints the leaderboard table to the screen
def seeleaderboard(leaderboard):
    print("The current leaderboard are as follows: \n")

    for position, player in enumerate(leaderboard, start=1):
        print str(position) + ". " + player
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
            seeleaderboard(leaderboard)
        elif choice == "5":
            quitProgram()
        else:
            print("Invalid input. \n")

# Adds a new player (Unix interface)
def clAddPlayers(players):
    if len(sys.argv) != 3:
        print("\n'-add' operator requires 1 parameter (name of player to be added)\n")
        sys.exit(1)
    
    players = readPlayers()
    newPlayer = sys.argv[2]

    addPlayerIfNew(players, newPlayer)

# Removes a player (Unix interface)
def clRemovePlayers(players, leaderboard):
    if len(sys.argv) != 3:
        print("\n'-remove' operator requires 1 parameter (name of player to be removed)\n")
        sys.exit(1)
    
    players = readPlayers()
    leaderboard = readLeaderboard()
    removedPlayer = sys.argv[2]

    removePlayerIfExists(players, leaderboard, removedPlayer)
    return

# Records a match between two players, updating the leaderboard table (Unix interface)
def clRecordMatch(players, leaderboard):
    if len(sys.argv) != 4:
        print("\n'-result' operator requires 2 parameters (name of winner, name of loser)\n")
        sys.exit(1)
    
    players = readPlayers()
    leaderboard = readLeaderboard()

    playersList = players.getPlayers()
    winner = Player(sys.argv[2])
    loser = Player(sys.argv[3])

    if winner not in playersList and loser not in playersList:
        print("Neither player is part of this league")
    elif winner not in playersList:
        print("The winner is not part of this league")
    elif loser not in playersList:
        print("The loser is not part of this league")
    else:
        updateLeaderboardAfterMatch(winner, loser, leaderboard)
        print("leaderboard updated!")



# Prints the current leaderboard to the terminal (Unix interface)
def clSeeleaderboard():
    if len(sys.argv) != 2:
        print("\n'-result' operator requires no parameters\n")
        sys.exit(1)
    
    leaderboard = readLeaderboard()
    seeleaderboard(leaderboard)





# Adds a player to the players list, unless they are already in the players list
def addPlayerIfNew(players, newPlayer):
    if (newPlayer.getName() in players):
            print("This player already exists.")
    else:
        addPlayer(players, newPlayer)
        print("Player added!")

# Adds player to end of players list
def addPlayer(players, newPlayer):
    players.append(newPlayer.getName())
    updatePlayers(players)

# Removes a player from the players list (and leaderboard list if they're in that list),
# unless they are not in the players list
def removePlayerIfExists(players, leaderboard, removedPlayer):
    if (removedPlayer not in players):
            print("This player is not in the league.")
    else:
        removePlayerFromPlayers(players, removedPlayer)
        if (removedPlayer in leaderboard):
            removePlayerFromleaderboard(leaderboard, removedPlayer)
        print("Player removed!")

# Removes player from players list
def removePlayerFromPlayers(players, playerToBeRemoved):
    players.remove(playerToBeRemoved)
    updatePlayers(players)

# Removes player from leaderboard list
def removePlayerFromleaderboard(leaderboard, playerToBeRemoved):
    leaderboard.remove(playerToBeRemoved)
    updateLeaderboard(leaderboard)

# Asks the user a yes/no question, returning false if anything
# but 'y' is entered
def askUserYNQuestion(question):
    print(question + " (y/n) \n")
    choice = raw_input()
    print("")
    if choice == "y":
        return False
    else:    # Stops the loop if anything but y entered
        return True

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
    leaderboardPlayers = leaderboard.getRankings()
    if winner not in leaderboardPlayers:
        leaderboard.append(winner)
    
    if loser not in leaderboardPlayers:
        leaderboard.append(loser)
    
    winner_position = leaderboardPlayers.index(winner)
    loser_position = leaderboardPlayers.index(loser)

    if winner_position > loser_position:
        leaderboardPlayers = leaderboard[:loser_position] + [winner] + leaderboard[loser_position:winner_position] + leaderboard[winner_position + 1:]
        leaderboard.setRankings(leaderboardPlayers)

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

def updatePlayers(players):
    updateFile("storedPlayers.txt", players)

def updateLeaderboard(leaderboard):
    updateFile("storedleaderboard.txt", leaderboard)

def updateFile(filename, leaderboard):
    myFile = open(filename, "w")
    for player in leaderboard.getRankings():
        myFile.write(player + "\n")
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