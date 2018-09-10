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
def addPlayers(players):
    finished = False

    while (not finished):
        print("Please enter the name of the new player: \n")
        newPlayer = raw_input()
        print("")

        if (newPlayer in players):
            print("This player already exists.")
            finished = anotherPlayerQuery(finished, "add")
        else:
            players.append(newPlayer)
            print("Player added!")
            finished = anotherPlayerQuery(finished, "add")

# Removes players from both the players list and the rankings list
def removePlayers(players, rankings):
    finished = False

    while (not finished):
        print("Please enter the name of the player you want to remove: \n")
        removedPlayer = raw_input()
        print("")

        if (removedPlayer not in players):
            print("This player is not in the league.")
            finished = anotherPlayerQuery(finished, "remove")
        else:
            players.remove(removedPlayer)
            if (removedPlayer in rankings):
                rankings.remove(removedPlayer)
            print("Player removed!")
            finished = anotherPlayerQuery(finished, "remove")

# Asks the user whether they want to add another user
def anotherPlayerQuery(finished, addOrRemove):
    finished2 = False
    while (not finished2):
        print("Would you like to " + addOrRemove + " another player? (y/n) \n")
        choice = raw_input()
        print("")
        if choice == "y":
            finished2 = True
        elif choice == "n":
            finished = True
            finished2 = True
        else:
            print("Invalid input.")
    return finished
 
# Allows the user to input a winner and loser of a match, and updates the rankings table
# accordingly
def recordMatch(players, rankings):
    winner = ""
    loser = ""
    
    finished = False
    while(not finished):
        print("Please enter the name of the match winner: \n")
        winner = raw_input()
        print("")

        if (winner not in players):
            print("This player is not in the league.")
        else:
            finished = True
    
    finished = False
    while(not finished):
        print("Please enter the name of the match loser: \n")
        loser = raw_input()
        print("")

        if (loser not in players):
            print("This player is not in the league.")
        else:
            finished = True

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

# Main method
def main():
    #players = ["matt", "junaid", "mike", "james", "sandeep"]
    #rankings = ["matt", "junaid", "mike", "james", "sandeep"]

    playersFile = open("storedPlayers.txt", "r")
    players = playersFile.read().splitlines()
    playersFile.close()
    
    rankingsFile = open("storedRankings.txt", "r")
    rankings = rankingsFile.read().splitlines()
    rankingsFile.close()

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
            addPlayers(players)
        elif choice == "2":
            removePlayers(players, rankings)
        elif choice == "3":
            rankings = recordMatch(players, rankings)
        elif choice == "4":
            seeRankings(rankings)
        elif choice == "5":
            quitProgram(players, rankings)
        else:
            print("Invalid input. \n")
        
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