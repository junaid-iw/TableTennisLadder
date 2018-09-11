import sys

# Called when the winner and loser are already on the rankings table
def existingWin(rankings, winner, loser):
    loser_position = rankings.index(loser)
    winner_position = rankings.index(winner)

    if winner_position > loser_position:
        rankings = rankings[:loser_position] + [winner] + rankings[loser_position:winner_position] + rankings[winner_position + 1:]

    return rankings

# Called when neither player is already on the rankings player
def newPlayers(rankings, winner, loser):
    rankings.append(winner)
    rankings.append(loser)
    
    return rankings

# Called when the winner is on the rankings table but the loser is not
def newLoser(rankings, loser):
    rankings.append(loser)
    
    return rankings

# Called when the loser is on the rankings table but the winner is not
def newWinner(rankings, winner, loser):
    loser_position = rankings.index(loser)
    rankings = rankings[:loser_position] + [winner] + rankings[loser_position:]
    
    return rankings

# Called when the user chooses to add a new player. Allows the user to add multiple players.
def addPlayersMenu(players):

    while (True):
        newPlayer = requestName("Please enter the name of the new player: \n")

        if (newPlayer in players):
            print("This player already exists.")
        else:
            addPlayer(players, newPlayer)
            print("Player added!")
            
        if askUserYNQuestion("Would you like to add another player?"):
            return players

# Removes players from both the players list and the rankings list
def removePlayersMenu(players, rankings):
    while (True):
        removedPlayer = requestName("Please enter the name of the player you want to remove: \n")

        if (removedPlayer not in players):
            print("This player is not in the league.")
        else:
            removePlayerFromPlayers(players, removedPlayer)
            if (removedPlayer in rankings):
                removePlayerFromRankings(rankings, removedPlayer)
            print("Player removed!")
        if askUserYNQuestion("Would you ike to remove another player?"):
            return players, rankings

# Allows the user to input a winner and loser of a match, and updates the rankings table
# accordingly
def recordMatchMenu(players, rankings):
    winner = requestWinnerOrLoser("winner", players)
    loser = requestWinnerOrLoser("loser", players)

    if winner in rankings and loser in rankings:
        rankings = existingWin(rankings, winner, loser)
    elif winner in rankings:
        rankings = newLoser(rankings, loser)
    elif loser in rankings:
        rankings = newWinner(rankings, winner, loser)
    else:
        rankings = newPlayers(rankings, winner, loser)

    print("Rankings updated!")
    return rankings

# Prints the rankings table to the screen
def seeRankings(rankings):
    print("The current rankings are as follows: \n")

    position = 1
    for player in rankings:
        print str(position) + ". " + player
        position += 1
    print("")

# Quits the program, updating the text files with the current players and rankings
def quitProgram(players, rankings):
    playersFile = open("storedPlayers.txt", "w")
    for player in players:
        playersFile.write(player + "\n")
    playersFile.close()

    rankingsFile = open("storedRankings.txt", "w")
    for player in rankings:
        rankingsFile.write(player + "\n")
    rankingsFile.close()

    print("Goodbye!")
    exit()

# Adds player to end of players list
def addPlayer(players, newPlayer):
    players.append(newPlayer)

# Removes player from players list
def removePlayerFromPlayers(players, playerToBeRemoved):
    players.remove(playerToBeRemoved)

# Removes player from rankings lists
def removePlayerFromRankings(rankings, playerToBeRemoved):
    rankings.remove(playerToBeRemoved)

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

def interactive(players, rankings):
    players = readPlayers()
    rankings = readRankings()

    print("Welcome to TZ Table Tennis (Copyright 2018. All rights reserved) \n")
    
    finished = False

    while (not finished):
        print("Please choose from one of the following options:")
        print("1) Add players")
        print("2) Remove players")
        print("3) Record match")
        print("4) See rankings")
        print("5) Exit \n")

        choice = raw_input()
        print("")

        if choice == "1":
            players = addPlayersMenu(players)
        elif choice == "2":
            players, rankings = removePlayersMenu(players, rankings)
        elif choice == "3":
            rankings = recordMatchMenu(players, rankings)
        elif choice == "4":
            seeRankings(rankings)
        elif choice == "5":
            quitProgram(players, rankings)
        else:
            print("Invalid input. \n")

# Method to add a new player using Unix-style interface
def clAddPlayers(players):
    if len(sys.argv) != 3:
        print("\n'-add' operator requires 1 parameter (name of player to be added)\n")
        sys.exit(1)
    
    players = readPlayers()
    newPlayer = sys.argv[2]

    if (newPlayer in players):
        print("\nThis player already exists.\n")
    else:
        playersFile = open("storedPlayers.txt", "a")
        playersFile.write(newPlayer)
        playersFile.close()
        print("\nPlayer added!\n")

# Method to record a match between two players, updating the rankings table, using
# Unix-style interface
def clRecordMatch(players, rankings):
    if len(sys.argv) != 4:
        print("\n'-result' operator requires 2 parameters (name of winner, name of loser)\n")
        sys.exit(1)



def clSeeRankings(): 
    return

def readPlayers():
    return readFile("storedPlayers.txt")

def readRankings():
    return readFile("storedRankings.txt")

def readFile(filename):
    myFile = open(filename, "r")
    contents = myFile.read().splitlines()
    myFile.close()
    return contents

def updatePlayers():
    return

def updateRankings():
    return

# Main method
def main():
    
    players = []
    rankings = []
    
    if len(sys.argv) == 1:
        clSeeRankings()
        sys.exit(1)

    if sys.argv[1] == "--interactive":
        interactive(players, rankings)
    elif sys.argv[1] == "-add":
        clAddPlayers(players)
    elif sys.argv[1] == "-result":
        clRecordMatch(players, rankings)
    elif sys.argv[1] == "-rank":
        clSeeRankings()
    else:
        print("Invalid input")

    
        
# def main():
#     if len(sys.argv) != 3:
#         print 'usage: ./rankings.py {winner | loser} file'
#         sys.exit(1)

#     rankings = ["matt", "junaid", "mike", "james", "sandeep"]
    
#     winner = sys.argv[1]
#     loser = sys.argv[2]

#     if winner in rankings and loser in rankings:
#         rankings = existingWin(rankings, winner, loser)
#     elif winner in rankings:
#         rankings = newLoser(rankings, loser)
#     elif loser in rankings:
#         rankings = newWinner(rankings, winner, loser)
#     else:
#         rankings = newPlayers(rankings, winner, loser)
#     #rankings = existingWin(rankings, "james", "matt")
#     #rankings = newLoser(rankings, "emily")
#     #rankings = newPlayers(rankings, "emily", "ash")
#     #rankings = newWinner(rankings, "emily", "junaid")

#     for player in rankings:
#         print(player)

if __name__ == '__main__':
  main()