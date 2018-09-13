import sys
from player import Player
from playersTable import PlayersTable
from leaderboard import Leaderboard


# # Called when the user chooses to add a new player. Allows the user to add multiple players.
# def addPlayersMenu(players):
#     while (True):
#         newPlayerName = requestName("Please enter the name of the new player: \n")
#         newPlayer = Player(newPlayerName)

#         addPlayerIfNew(players, newPlayer)
            
#         if not askUserYNQuestion("Would you like to add another player?"):
#             return players

# # Removes players from both the players list and the leaderboard list
# def removePlayersMenu(playersList, leaderboard):
#     while (True):
#         removedPlayerName = requestName("Please enter the name of the player you want to remove: \n")
#         removedPlayer = Player(removedPlayerName)

#         removePlayerIfInPlayersTable(playersList, leaderboard, removedPlayer)

#         if not askUserYNQuestion("Would you ike to remove another player?"):
#             return playersList, leaderboard

# # Allows the user to input a winner and loser of a match, and updates the leaderboard table
# # accordingly
# def recordMatchMenu(players, leaderboard):
#     winner = requestWinnerOrLoser("winner", players)
#     loser = requestWinnerOrLoser("loser", players)
#     leaderboard = updateLeaderboardAfterMatch(winner, loser, leaderboard)

#     print("leaderboard updated!")
#     return leaderboard

# # Quits the program
# def quitProgram():
#     print("Goodbye!")
#     exit()

# # Starts the interactive mode of the program
# def clInteractive(players, leaderboard):
#     players = readPlayers()
#     leaderboard = readLeaderboard("storedLeaderboard")

#     print("Welcome to TZ Table Tennis (Copyright 2018. All rights reserved) \n")
    
#     finished = False

#     while (not finished):
#         print("Please choose from one of the following options:")
#         print("1) Add players")
#         print("2) Remove players")
#         print("3) Record match")
#         print("4) See leaderboard")
#         print("5) Exit \n")

#         choice = raw_input()
#         print("")

#         if choice == "1":
#             players = addPlayersMenu(players)
#         elif choice == "2":
#             players, leaderboard = removePlayersMenu(players, leaderboard)
#         elif choice == "3":
#             leaderboard = recordMatchMenu(players, leaderboard)
#         elif choice == "4":
#             seeLeaderboard(leaderboard)
#         elif choice == "5":
#             quitProgram()
#         else:
#             print("Invalid input. \n")






# Adds a new player (Unix interface)
def clAddPlayers(playersTable):
    if len(sys.argv) != 3:
        print("\n'--add' operator requires 1 parameter (name of player to be added)\n")
        sys.exit(1)
    
    playersTable = readPlayers()
    newPlayerName = sys.argv[2]
    newPlayer = Player(newPlayerName)

    addPlayerIfNew(playersTable, newPlayer)

# Removes a player from the current leaderboard
def clRemovePlayerFromAll(players, leaderboard):
    if len(sys.argv) != 3:
        print("\n'--removeall' operator requires 1 parameters (the player to be removed)\n")
        sys.exit(1)
    
    playersTable = readPlayers()
    
    removedPlayerName = sys.argv[2]
    removedPlayer = Player(removedPlayerName)

    if not playersTable.playerInTable(removedPlayer):
        print("This player is not in the players list.")
    else:
        removePlayerFromAll(playersTable, removedPlayer)


# Removes a player from all leaderboards and players table (Unix interface)
def clRemovePlayer(players, leaderboard):
    if len(sys.argv) != 3:
        print("\n'--remove' operator requires 1 parameter (the player to be removed)\n")
        sys.exit(1)
    
    playersTable = readPlayers()
    
    removedPlayerName = sys.argv[2]
    removedPlayer = Player(removedPlayerName)

    if not playersTable.playerInTable(removedPlayer):
        print("This player is not in the players list.")
    else:
        leaderboard = getCurrentLeaderboard()
        removePlayerFromLeaderboardIfPresent(leaderboard, removedPlayer)

# Records a match between two players, updating the leaderboard table (Unix interface)
def clRecordMatch(playersTable, leaderboard):
    if len(sys.argv) != 4:
        print("\n'--result' operator requires 2 parameters (name of winner, name of loser)\n")
        sys.exit(1)
    
    playersTable = readPlayers()
    leaderboard = getCurrentLeaderboard()

    winner = Player(sys.argv[2])
    loser = Player(sys.argv[3])

    if winner == loser:
        print("The winner and loser must be different players")
    elif not playersTable.playerInTable(winner) and playersTable.playerInTable(loser):
        print("Neither player is part of this league")
    elif not playersTable.playerInTable(winner):
        print("The winner is not part of this league")
    elif not playersTable.playerInTable(loser):
        print("The loser is not part of this league")
    else:
        updateLeaderboardAfterMatch(winner, loser, leaderboard)
        print("Leaderboard updated!")

def defaultSeeLeaderboard():
    leaderboard = getCurrentLeaderboard()
    seeLeaderboard(leaderboard)

# Prints the current leaderboard to the terminal (Unix interface)
def clSeeLeaderboard():
    if len(sys.argv) != 2:
        print("\n'--rank' operator requires no parameters\n")
        sys.exit(1)
    
    leaderboard = getCurrentLeaderboard()
    seeLeaderboard(leaderboard)

# Changes to a new current leaderboard
def clChangeLeaderboard():
    if len(sys.argv) != 3:
        print("\n'--change' operator requires 1 parameter (the leaderboard to be changed to)\n")
        sys.exit(1)

    newCurrentLeaderboardName = sys.argv[2]
    currentLeaderboard = getCurrentLeaderboard()
    leaderboardNames = readLeaderboardNames()
    if newCurrentLeaderboardName not in leaderboardNames:
        print("The specified leaderboard does not exist")
    elif newCurrentLeaderboardName == currentLeaderboard.getName():
        print("The specified leaderboard is already the current leaderboard")
    else:
        reorderLeaderboardNames(newCurrentLeaderboardName, leaderboardNames)
        print("Current leaderboard changed to " + newCurrentLeaderboardName)

# Creates a new leaderboard and makes it the current leaderboard
def clNewLeaderboard():
    if len(sys.argv) != 3:
        print("\n'--new' operator requires 1 parameter (the leaderboard to be changed to)\n")
        sys.exit(1)
    
    newLeaderboardName = sys.argv[2]
    leaderboardNames = readLeaderboardNames()

    if newLeaderboardName in leaderboardNames:
        print("This leaderboard already exists")
    else:
        newLeaderboard = Leaderboard(newLeaderboardName, [])
        updateLeaderboard(newLeaderboard)

        reorderLeaderboardNames(newLeaderboardName, leaderboardNames)
        print("Leaderboard added!")

# Displays the help menu
def clShowHelp():
    helpFile = open("help.txt", "r")
    helpFileContents = helpFile.read()
    print(helpFileContents)


# Adds a player to the players list, unless they are already in the players list
def addPlayerIfNew(playersTable, newPlayer):
    if playersTable.playerInTable(newPlayer):
            print("This player already in the players list.")
    else:
        playersTable.addPlayer(newPlayer)
        updatePlayersTable(playersTable)
        print("Player added!")    

# Removes a player from the players list (and leaderboard list if they're in that list),
# unless they are not in the players list
def removePlayerFromAll(playersTable, removedPlayer):
    removePlayerFromPlayersTable(playersTable, removedPlayer)
    
    leaderboardNames = readLeaderboardNames()
    for leaderboardName in leaderboardNames:
        leaderboard = readLeaderboard(leaderboardName)
        if leaderboard.playerInRankings(removedPlayer):
            removePlayerFromLeaderboard(leaderboard, removedPlayer)
    print("Player removed from championship!")

def removePlayerFromLeaderboardIfPresent(leaderboard, removedPlayer):
    if leaderboard.playerInRankings(removedPlayer):
        removePlayerFromLeaderboard(leaderboard, removedPlayer)
        print("Player removed from " + leaderboard.getName())
    else:
        print("This player is not in the specified leaderboard")

# Removes player from players table
def removePlayerFromPlayersTable(playersTable, removedPlayer):
    playersTable.removePlayer(removedPlayer)
    updatePlayersTable(playersTable)

# Removes player from leaderboard
def removePlayerFromLeaderboard(leaderboard, removedPlayer):
    leaderboard.removePlayer(removedPlayer)
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

# Reorders the leaderboardNames.txt file so the current leaderboard's name is first
def reorderLeaderboardNames(newCurrentLeaderboardName, leaderboardNames):
    if newCurrentLeaderboardName in leaderboardNames:
        newCurrentLearderboardNamePosition = leaderboardNames.index(newCurrentLeaderboardName)
        reorderedLeaderboardNames = [newCurrentLeaderboardName] + leaderboardNames[:newCurrentLearderboardNamePosition] + leaderboardNames[newCurrentLearderboardNamePosition + 1:]
    else:
        reorderedLeaderboardNames = [newCurrentLeaderboardName] + leaderboardNames
    updateFile("leaderboardNames.txt", reorderedLeaderboardNames)

# Prints the leaderboard table to the screen
def seeLeaderboard(leaderboard):
    print(leaderboard.getName() +  ":\n")
    
    players = leaderboard.getRankings()
    if len(players) == 0:
        print("There are currently no players on this leaderboard")
    else:
        for position, player in enumerate(players, start=1):
            print str(position) + ". " + player.getName()
    
    print("")

def getAllLeaderboards():
    leaderboardNames = readLeaderboardNames()
    allLeaderboards = []

    for name in leaderboardNames:
        leaderboard = readLeaderboard(name)
        allLeaderboards.append(leaderboard)

    return allLeaderboards

# Returns the current leaderboard
def getCurrentLeaderboard():
    leaderboardNames = readLeaderboardNames()
    if len(leaderboardNames) == 0:
        print("There are currently no existing leaderboards")
        sys.exit(1)

    currentLeaderboardName = leaderboardNames[0]
    currentLeaderboard = readLeaderboard(currentLeaderboardName)
    return currentLeaderboard

def readPlayers():
    playerNames = readFile("storedPlayers.txt")
    players = []
    for name in playerNames:
        player = Player(name)
        players.append(player)
    playersTable = PlayersTable(players)
    return playersTable

def readLeaderboard(leaderboardName):
    playerNames = readFile(leaderboardName + ".txt")
    players = []
    for name in playerNames:
        player = Player(name)
        players.append(player)
    leaderboard = Leaderboard(leaderboardName, players)
    return leaderboard

def readLeaderboardNames():
    leaderboardNames = readFile("leaderboardNames.txt")
    return leaderboardNames

def readFile(filename):
    myFile = open(filename, "r")
    contents = myFile.read().splitlines()
    myFile.close()
    return contents

def updatePlayersTable(playersTable):
    players = playersTable.getPlayers()
    playerNames = []
    for player in players:
        playerNames.append(player.getName())
    updateFile("storedPlayers.txt", playerNames)

def updateLeaderboard(leaderboard):
    players = leaderboard.getRankings()
    playerNames = []
    for player in players:
        playerNames.append(player.getName())
    leaderboardName = leaderboard.getName()
    updateFile(leaderboardName + ".txt", playerNames)

def updateFile(filename, contents):
    myFile = open(filename, "w")
    for item in contents:
        myFile.write(item + "\n")
    myFile.close()


def updateHTML():
    #Create list of leaderboard objects
    #Search for bit to be replaced
    #Loop through leaderboard list, adding each leaderboard
        #Loop through players in leaderboard, adding each player

    with open('startFile.html', 'r') as myfile:
        htmlString = myfile.read()
        myfile.close()
    
    allLeaderboards = getAllLeaderboards()

    for leaderboard in allLeaderboards:

        htmlString += '\n<div class="leaderboard">'
        htmlString += '\n<span style="position: relative; top: -80px; font-size: 150px;">&#x1F3C6;</span>'
        htmlString += '\n<h1 style="margin-top: -50px">'+ leaderboard.getName() +'</h1>'
        htmlString += '\n<div id="results">'
        
        players = leaderboard.getRankings()
        if len(players) == 0:
            htmlString += '<p>There are currently no players on this leaderboard</p>'
        else:
            htmlString += '\n<div class="row"><div style="margin: 0; padding: 0; float:left;">1.</div> <marquee width="190px">'+ players[0].getName() +'</marquee> <div style="vertical-align: middle; font-size: 26px; height: 44px; width: 44px; background-color: white; border-radius: 50px; float: right; margin: 0; padding: 0;"><p style="margin-top: 6px;">&#x1F3C6;</p></div></div>'

            for position, player in enumerate(players, start=1):
                if not position == 1:
                    htmlString += '<div class="row"><div style="margin: 0; padding: 0; float:left;">' + str(position) + '.</div>' + player.getName() + '</div>'

        htmlString += '\n</div>\n</div>'

    htmlString += '\n</div>\n</body>\n</html>'
        
    f= open("leaderboard.html","w")
    f.write(htmlString)
    f.close()



# Main method
def main():
    
    players = []
    leaderboard = []
    
    if len(sys.argv) == 1:
        defaultSeeLeaderboard()
        sys.exit(1)
    operator = sys.argv[1]
    if operator == "--add":
        clAddPlayers(players)
    elif operator == "--remove":
        clRemovePlayer(players, leaderboard)
    elif operator == "--removeall":
        clRemovePlayerFromAll(players, leaderboard)
    elif operator == "--result":
        clRecordMatch(players, leaderboard)
    elif operator == "--rank":
        clSeeLeaderboard()
    elif operator == "--change":
        clChangeLeaderboard()
    elif operator == "--new":
        clNewLeaderboard()
    elif operator == "--help":
        clShowHelp()
    else:
        print("Invalid input")

    updateHTML()



if __name__ == '__main__':
  main()