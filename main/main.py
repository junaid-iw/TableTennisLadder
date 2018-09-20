import os
import sys
sys.path.append('../')
from player.player import Player
from players_table.playersTable import PlayersTable
from leaderboard.leaderboard import Leaderboard
from flask import Flask, render_template, request, redirect, url_for



# Main method
def main():
    players = []
    leaderboard = []
    
    if len(sys.argv) == 1:
        defaultSeeLeaderboard()
        sys.exit(1)
    operator = sys.argv[1]
    if operator == "--add_player":
        addPlayer(players)
    elif operator == "--rm_player":
        removePlayer(players, leaderboard)
    elif operator == "--rm_player_all":
        removePlayerFromAll(players, leaderboard)
    elif operator == "--result":
        recordMatch(players, leaderboard)
    elif operator == "--rank":
        seeLeaderboard()
    elif operator == "--change":
        changeLeaderboard()
    elif operator == "--add_board":
        createLeaderboard()
    elif operator == "--rm_board":
        removeLeaderboard()
    elif operator == "--help":
        showHelp()
    else:
        print("Invalid input")


#
# ADD PLAYER METHODS
#

# Adds a new player (Unix interface)
def addPlayer(playersTable):
    if len(sys.argv) != 3:
        print("\n'--add' operator requires 1 parameter (name of player to be added)\n")
        sys.exit(1)
    
    playersTable = readPlayers()
    newPlayerName = sys.argv[2]
    newPlayer = Player(newPlayerName)

    addPlayerIfNew(playersTable, newPlayer)

# Adds a player to the players list, unless they are already in the players list
def addPlayerIfNew(playersTable, newPlayer):
    if playersTable.playerInTable(newPlayer):
            print("This player already in the players list.")
    else:
        playersTable.addPlayer(newPlayer)
        updatePlayersTable(playersTable)
        print("Player added!")   

#
# REMOVE PLAYER METHODS
#

# Removes a player from the current leaderboard
def removePlayerFromAll(players, leaderboard):
    if len(sys.argv) != 3:
        print("\n'--removeall' operator requires 1 parameters (the player to be removed)\n")
        sys.exit(1)
    
    playersTable = readPlayers()
    
    removedPlayerName = sys.argv[2]
    removedPlayer = Player(removedPlayerName)

    if not playersTable.playerInTable(removedPlayer):
        print("This player is not in the players list.")
    else:
        deletePlayerFromAll(playersTable, removedPlayer)
        print("Player removed from championship!")

# Removes a player from all leaderboards and players table (Unix interface)
def removePlayer(players, leaderboard):
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

# Removes a player from the players list (and leaderboard list if they're in that list),
# unless they are not in the players list
def deletePlayerFromAll(playersTable, removedPlayer):
    removePlayerFromPlayersTable(playersTable, removedPlayer)
    
    leaderboardNames = readLeaderboardNames()
    for leaderboardName in leaderboardNames:
        leaderboard = readLeaderboard(leaderboardName)
        if leaderboard.removePlayer(removedPlayer):
            updateLeaderboard(leaderboard)


# Removes a specified player from the current leaderboard if they are on that leaderboard
def removePlayerFromLeaderboardIfPresent(leaderboard, removedPlayer):
    if leaderboard.removePlayer(removedPlayer):
        updateLeaderboard(leaderboard)
        print("Player removed from " + leaderboard.getName())
    else:
        print("This player is not in the specified leaderboard")

    # if leaderboard.playerInRankings(removedPlayer):
    #     removePlayerFromLeaderboard(leaderboard, removedPlayer)
    #     print("Player removed from " + leaderboard.getName())
    # else:
    #     print("This player is not in the specified leaderboard")

# Removes player from players table
def removePlayerFromPlayersTable(playersTable, removedPlayer):
    playersTable.removePlayer(removedPlayer)
    updatePlayersTable(playersTable)

# Removes player from leaderboard
def removePlayerFromLeaderboard(leaderboard, removedPlayer):
    leaderboard.removePlayer(removedPlayer)
    updateLeaderboard(leaderboard)

#
# RECORD MATCH METHODS
#

# Records a match between two players, updating the leaderboard table (Unix interface)
def recordMatch(winner, loser):
    playersTable = readPlayers()
    leaderboard = getCurrentLeaderboard()
    winner = Player(winner)
    loser = Player(loser)

    if winner.name == loser.name:
        return False

    elif not playersTable.playerInTable(winner) and playersTable.playerInTable(loser):
        playersTable.players.append(winner)
        playersTable.players.append(loser)

    elif winner not in playersTable.players:
        playersTable.players.append(winner)

    elif not playersTable.playerInTable(loser):
        playersTable.players.append(loser)

    updateLeaderboardAfterMatch(winner, loser, leaderboard)

# Updates the leaderboard list based on a winner and loser of a match
def updateLeaderboardAfterMatch(winner, loser, leaderboard):
    leaderboard.updateAfterMatch(winner, loser)

    updateLeaderboard(leaderboard)
    return leaderboard

#
# SEE LEADERBOARD METHODS
#

def defaultSeeLeaderboard():
    leaderboard = getCurrentLeaderboard()
    printLeaderboard(leaderboard)

# Prints the current leaderboard to the terminal (Unix interface)
def seeLeaderboard():
    if len(sys.argv) != 2:
        print("\n'--rank' operator requires no parameters\n")
        sys.exit(1)
    
    leaderboard = getCurrentLeaderboard()
    printLeaderboard(leaderboard)

# Prints the leaderboard table to the screen
def printLeaderboard(leaderboard):
    print(leaderboard.getName() +  ":\n")
    
    players = leaderboard.getRankings()
    if len(players) == 0:
        print("There are currently no players on this leaderboard")
    else:
        for position, player in enumerate(players, start=1):
            print str(position) + ". " + player.getName()
    
    print("")

#
# CHANGE LEADERBOARD METHODS
#

# Changes to a new current leaderboard
def changeLeaderboard():
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

#
# CREATE LEADERBOARD METHODS
#

# Creates a new leaderboard and makes it the current leaderboard
def createLeaderboard():
    if len(sys.argv) != 3:
        print("\n'--new' operator requires 1 parameter (the leaderboard to be changed to)\n")
        sys.exit(1)
    
    newLeaderboardName = sys.argv[2]
    leaderboardNames = readLeaderboardNames()

    if newLeaderboardName in leaderboardNames:
        print("This leaderboard already exists")
    elif newLeaderboardName == "leaderboardNames":
        print("This name is not permitted")
    else:
        newLeaderboard = Leaderboard(newLeaderboardName, [])
        updateLeaderboard(newLeaderboard)

        reorderLeaderboardNames(newLeaderboardName, leaderboardNames)
        print("Leaderboard added!")

#
# REMOVE LEADERBOARD METHODS
#

# Removes a specified leaderboard if it exists
def removeLeaderboard():
    if len(sys.argv) != 3:
        print("\n'--new' operator requires 1 parameter (the leaderboard to be changed to)\n")
        sys.exit(1)
    
    removedLeaderboardName = sys.argv[2]
    leaderboardNames = readLeaderboardNames()

    if removedLeaderboardName not in leaderboardNames:
        print("This leaderboard does not exist")
    else:
        deleteLeaderboard(removedLeaderboardName)
        print("Leaderboard removed!")

# Removes a specified leaderboard
def deleteLeaderboard(removedLeaderboardName):
    leaderboardNames = readLeaderboardNames()
    leaderboardNames.remove(removedLeaderboardName)
    os.remove("../leaderboard/" + removedLeaderboardName + ".txt")
    updateLeaderboardNames(leaderboardNames)    

#
# SHOW HELP METHODS
#

# Displays the help menu
def showHelp():
    helpFile = open("../help.txt", "r")
    helpFileContents = helpFile.read()
    print(helpFileContents)


#
# AUXILLARY METHODS
#

# Asks the user a yes/no question, returning false if anything but 'y' is entered
# THIS IS FOR INTERACTIVE MODE
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

# Returns a list of all the leaderboards
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

    currentLeaderboardName = leaderboardNames[0]
    currentLeaderboard = readLeaderboard(currentLeaderboardName)
    return currentLeaderboard

#
# READ FILE METHODS
#

def readPlayers():
    playerNames = readFile("../player/storedPlayers.txt")
    players = []

    for name in playerNames:
        player = Player(name)
        players.append(player)

    playersTable = PlayersTable(players)

    return playersTable

def readLeaderboard(leaderboardName):
    playerNames = readFile("../leaderboard/" + leaderboardName + ".txt")
    players = []
    for name in playerNames:
        player = Player(name)
        players.append(player)
    leaderboard = Leaderboard(leaderboardName, players)
    return leaderboard

def readLeaderboardNames():
    leaderboardNames = readFile("../leaderboard/leaderboardNames.txt")
    return leaderboardNames

def readFile(filename):
    myFile = open(filename, "r")
    contents = myFile.read().splitlines()
    myFile.close()
    return contents

#
# WRITE FILE METHODS
#

def updatePlayersTable(playersTable):
    players = playersTable.getPlayers()
    playerNames = []
    for player in players:
        playerNames.append(player.getName())
    updateFile("../player/storedPlayers.txt", playerNames)

def updateLeaderboard(leaderboard):
    players = leaderboard.getRankings()
    playerNames = []
    for player in players:
        playerNames.append(player.getName())
    leaderboardName = leaderboard.getName()
    updateFile("../leaderboard/" + leaderboardName + ".txt", playerNames)

def updateLeaderboardNames(leaderboardNames):
    updateFile("../leaderboard/leaderboardNames.txt", leaderboardNames)

# Reorders the leaderboardNames.txt file so the current leaderboard's name is first
def reorderLeaderboardNames(newCurrentLeaderboardName, leaderboardNames):
    if newCurrentLeaderboardName in leaderboardNames:
        newCurrentLearderboardNamePosition = leaderboardNames.index(newCurrentLeaderboardName)
        reorderedLeaderboardNames = [newCurrentLeaderboardName] + leaderboardNames[:newCurrentLearderboardNamePosition] + leaderboardNames[newCurrentLearderboardNamePosition + 1:]
    else:
        reorderedLeaderboardNames = [newCurrentLeaderboardName] + leaderboardNames
    updateFile("../leaderboard/leaderboardNames.txt", reorderedLeaderboardNames)

def updateFile(filename, contents):
    myFile = open(filename, "w")
    for item in contents:
        myFile.write(item + "\n")
    myFile.close()


if __name__ == "__main__":
    main()

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/leaderboard')
def leaderboard():
    leaderboards = getAllLeaderboards()

    lb_list = []

    for l in leaderboards:
        player_list = []
        for p in l.rankings:
            player_list.append([p, l.rankings.index(p) + 1])
        lb_list.append([l.name, player_list])

    return render_template('lb.html', leaderboards=lb_list)


@app.route('/addresult')
def add_form():
    return render_template('add_result_form.html')


@app.route('/addresult', methods=['POST'])
def add_result():
    multiselect = request.form.getlist('player')
    winner = multiselect[0].capitalize()
    loser = multiselect[1].capitalize()
    recordMatch(winner, loser)

    return redirect(url_for("leaderboard"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

